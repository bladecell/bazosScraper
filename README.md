# Bazos Scraper API

A Flask-based REST API that provides endpoints for scraping listings from Bazos marketplace. The API supports both synchronous and asynchronous search operations with customizable search parameters.

## Features

- Search listings with customizable parameters
- Synchronous and asynchronous operation modes
- CORS support for cross-origin requests
- Flexible price range filtering
- Distance-based location filtering
- Customizable results limit
- Sorting options

## Installation

### Using Docker (Recommended)

Pull and run the Docker image:
```bash
docker pull bladecell/bazos-scraper-api
docker run -p 5000:5000 bladecell/bazos-scraper-api
```

### Manual Installation

1. Clone the repository
2. Install dependencies using the requirements.txt file:
```bash
pip install -r requirements.txt
```

## Requirements

All dependencies are listed in `requirements.txt`:
```
flask
flask-cors
# Additional dependencies from requirements.txt
```

## Docker Support

The project includes a Dockerfile for containerized deployment. You can build the image locally:

```bash
docker build -t bazos-scraper-api .
docker run -p 5000:5000 bazos-scraper-api
```

Or use the pre-built image from Docker Hub:
```bash
docker pull bladecell/bazos-scraper-api
```

## API Endpoints

### 1. Synchronous Search
```
GET /api/search
```

### 2. Asynchronous Search
```
GET /api/async_search
```

Both endpoints accept the following query parameters:

| Parameter     | Type    | Default | Description                           |
|--------------|---------|---------|---------------------------------------|
| search       | string  | ''      | Search query text                     |
| location     | string  | null    | Location for search                   |
| distance     | string  | '25'    | Search radius in kilometers           |
| min_price    | integer | null    | Minimum price filter                  |
| max_price    | integer | null    | Maximum price filter                  |
| order        | integer | null    | Sort order for results                |
| results_limit| integer | null    | Maximum number of results to return   |

## Usage Examples

### Basic Search
```
GET /api/search?search=iphone&location=Prague
```

### Advanced Search with Filters
```
GET /api/search?search=car&location=Brno&distance=50&min_price=1000&max_price=5000&order=1&results_limit=20
```

### Asynchronous Search
```
GET /api/async_search?search=laptop&location=Ostrava
```

## Response Format

The API returns a JSON array of listings, where each listing contains the scraped data from Bazos.

Example response:
```json
[
    {
        "title": "Item Title",
        "price": 1000,
        "location": "Prague",
        "url": "https://bazos.cz/item/123"
        // ... additional listing details
    }
]
```

## Running the Server

### Using Docker
```bash
docker run -p 5000:5000 bladecell/bazos-scraper-api
```

### Manual Run
```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

## Dependencies

- Flask
- Flask-CORS
- BazosScraper (custom scraping module)
- asyncio
- Additional dependencies as specified in requirements.txt

## Note

This API requires the `BazosScraper` class implementation, which should be provided in a separate file named `BazosScraper.py`. Ensure the scraper class implements the required methods and properties referenced in the API code.
