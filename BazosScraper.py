import urllib.parse
import urllib.request
import re
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass, asdict, field
from typing import List, Optional
from tqdm import tqdm

@dataclass
class Listing:
    link: str = ''
    img_link: str = ''
    added: str = ''
    description: str = ''
    price: int = 0
    currency: str = ''
    location: str = ''
    post_code: str = ''
    views: int = 0

    @classmethod
    def from_html(cls, inzeratyflex):
        def safe_get_text(element, separator=''):
            return element.get_text(separator=separator).strip() if element else ''

        def safe_get_int(element, separator=''):
            if element:
                el_str = "".join(re.findall(r'\d+', safe_get_text(element, separator)))
                return int(el_str) if el_str else 0
            return 0

        def safe_get_attr(element, attr):
            return element.get(attr, '').strip() if element else ''

        return cls(
            link=safe_get_attr(inzeratyflex.find('h2').find('a'), 'href'),
            img_link=safe_get_attr(inzeratyflex.find('a').find('img'), 'src'),
            added="".join(re.findall('[0-9.]', safe_get_text(inzeratyflex.find('span')))),
            description=safe_get_text(inzeratyflex.find("div", {"class": "popis"})),
            price=safe_get_int(inzeratyflex.find("div", {"class": "inzeratycena"})),
            currency="".join(re.findall(r'[^\d.]', safe_get_text(inzeratyflex.find("div", {"class": "inzeratycena"})))).strip(),
            location="".join(re.findall(r'[^\d.]', safe_get_text(inzeratyflex.find("div", {"class": "inzeratylok"})))).strip(),
            post_code="".join(re.findall(r'\d{3}\s\d{2}', safe_get_text(inzeratyflex.find("div", {"class": "inzeratylok"})))),
            views=safe_get_int(inzeratyflex.find("div", {"class": "inzeratyview"}))
        )

@dataclass
class ListingList:
    listings: List[Listing] = field(default_factory=list)

    def add_listing(self, inzeratyflex):
        self.listings.append(Listing.from_html(inzeratyflex))

    def to_dict_list(self):
        return [asdict(item) for item in self.listings]

    def to_json(self, indent=2):
        return json.dumps(self.to_dict_list(), ensure_ascii=False, indent=indent)

    def get(self, attr):
        return [getattr(item, attr) for item in self.listings]

class BazosScraper:
    BASE_URL = "https://www.bazos.cz/search.php"

    def __init__(self, search: str, location: Optional[str] = None, distance: int = 25,
                 min_price: Optional[int] = None, max_price: Optional[int] = None,
                 order: Optional[int] = None, start_index: Optional[int] = None,
                 results_limit: Optional[int] = None):
        self.search_params = {
            "search": search,
            "location": location,
            "distance": distance,
            "min_price": min_price,
            "max_price": max_price,
            "order": order,
            "start_index": start_index,
        }
        self.results_limit = results_limit
        self.listings = ListingList()

    def _build_url(self, **kwargs) -> str:
        query_params = {
            "hledat": self.search_params["search"],
            "rubriky": "www",
            "hlokalita": self.search_params["location"] or "",
            "humkreis": self.search_params["distance"],
            "cenaod": self.search_params["min_price"] or "",
            "cenado": self.search_params["max_price"] or "",
            "order": self.search_params["order"] or "",
            "kitx": "ano",
            "crz": kwargs.get("index", ""),
            "Submit": "Hledat"
        }
        filtered_query_params = {k: v for k, v in query_params.items() if v or k == "Submit"}
        return f"{self.BASE_URL}?{urllib.parse.urlencode(filtered_query_params)}"

    def _get_soup(self, **kwargs):
        with urllib.request.urlopen(self._build_url(**kwargs)) as response:
            html = response.read().decode("utf-8")
        return BeautifulSoup(html, 'html.parser')

    def scrape(self):
        soup = self._get_soup()
        results_count = int(soup.find('div', class_='inzeratynadpis').text.split()[-1])
        total_results = min(results_count, self.results_limit or float('inf'))
        total_pages = (total_results + 19) // 20

        with tqdm(total=total_results, desc="Scraping listings", unit="listing") as pbar:
            for page in range(total_pages):
                soup = self._get_soup(index=str(page * 20))
                inzeraty = soup.find_all("div", {"class": "inzeraty inzeratyflex"})
                for inzerat in inzeraty:
                    if pbar.n >= total_results:
                        return
                    self.listings.add_listing(inzerat)
                    pbar.update(1)

    def to_json(self):
        return self.listings.to_json()


if __name__ == "__main__":
    scraper = BazosScraper("Ryzen", location="Brno", min_price=5000, max_price=20000, results_limit=100)
    scraper.scrape()
    print(scraper.to_json())