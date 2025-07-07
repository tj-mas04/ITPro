# Indian High Courts Judgments Scraper

This is a FastAPI-based web scraper for retrieving judgments from various High Courts of India. The application provides a REST API interface to fetch judgments based on court name, date range, and other parameters.

## Features

- Scrape judgments from multiple High Courts of India
- REST API interface for easy integration
- Support for date-based filtering
- Asynchronous scraping for better performance
- Error handling and logging

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

1. `GET /`: Welcome message
2. `GET /courts`: List of available courts
3. `GET /judgments/{court_name}`: Get judgments from a specific court
   - Query parameters:
     - `start_date`: Start date (YYYY-MM-DD)
     - `end_date`: End date (YYYY-MM-DD)
     - `limit`: Maximum number of judgments to return (default: 10)

## Supported Courts

- Supreme Court of India
- Delhi High Court
- Bombay High Court
- Madras High Court
- Calcutta High Court
- Karnataka High Court
- Kerala High Court
- Gujarat High Court
- Punjab and Haryana High Court
- Allahabad High Court

## Contributing

Feel free to contribute to this project by:
1. Adding support for more courts
2. Improving the scraping logic
3. Adding new features
4. Reporting bugs

## License

This project is licensed under the MIT License. 