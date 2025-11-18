# Invoice Calculator Microservice

A Python microservice built with FastAPI for calculating invoice totals, including subtotals, taxes (IVA), and discounts based on business rules.

## Architecture

This microservice follows a **Clean Architecture** pattern with clear separation of concerns across four main layers:

### Layer Structure

```
microservice-python/
├── domain/              # Business logic and domain models
│   ├── model.py        # Pydantic models (Item, InvoiceCalculationResult)
│   └── rules.py        # Business rules (subtotal, taxes, discounts calculation)
├── application/         # Application services and use cases
│   ├── services.py     # InvoiceCalculatorService (orchestrates domain logic)
│   └── mappers.py      # Data transformation (domain → DTOs)
├── infrastructure/     # External concerns and framework setup
│   ├── fastapi_app.py  # FastAPI application factory
│   ├── config.py       # Application configuration
│   └── auth.py         # Authentication middleware
├── presentation/       # API layer (HTTP endpoints)
│   └── routes.py       # FastAPI routes and request handlers
└── tests/              # Test suite
    └── test_calculator.py
```

### Architecture Principles

- **Domain Layer**: Contains pure business logic, independent of frameworks
- **Application Layer**: Orchestrates domain operations and coordinates use cases
- **Infrastructure Layer**: Handles external concerns (FastAPI, authentication, configuration)
- **Presentation Layer**: Exposes HTTP endpoints and handles request/response

## Features

- ✅ Invoice calculation with subtotal, taxes (IVA 19%), and discounts
- ✅ Business rule: 5% discount for orders over 1000
- ✅ Token-based authentication (X-API-Token header)
- ✅ Comprehensive test coverage
- ✅ Docker support
- ✅ RESTful API with OpenAPI documentation

## Installation

### Prerequisites

- Python 3.13+
- pip

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export TOKEN_SECRET="your-secret-token-here"
   ```

   On Windows:
   ```powershell
   $env:TOKEN_SECRET="your-secret-token-here"
   ```

## Usage

### Running the Service

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### API Endpoint

#### Calculate Invoice

**POST** `/calculate`

Calculate invoice total from a list of items.

**Headers:**
```
X-API-Token: your-secret-token
```

**Request Body:**
```json
[
  {
    "product": "Product A",
    "unit_price": 100.0,
    "quantity": 2
  },
  {
    "product": "Product B",
    "unit_price": 50.0,
    "quantity": 1
  }
]
```

**Response:**
```json
{
  "subtotal": 250.0,
  "taxes": 47.5,
  "discounts": 0.0,
  "total": 297.5
}
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/calculate" \
  -H "X-API-Token: your-secret-token" \
  -H "Content-Type: application/json" \
  -d '[
    {"product": "A", "unit_price": 100, "quantity": 2},
    {"product": "B", "unit_price": 50, "quantity": 1}
  ]'
```

### Business Rules

- **Subtotal**: Sum of (unit_price × quantity) for all items
- **Taxes (IVA)**: 19% of subtotal
- **Discounts**: 5% of subtotal if subtotal > 1000, otherwise 0
- **Total**: subtotal + taxes - discounts

## Testing

### Run Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=./ --cov-report=xml -v
```

### Test Coverage

The test suite includes:

**Service Layer Tests:**
- Basic calculation
- Calculation with discount
- Single item calculation
- Zero quantity handling
- Empty list handling
- Discount threshold testing

**API Endpoint Tests:**
- Successful requests with valid token
- Authentication failures (missing token, invalid token)
- Discount calculation via API
- Edge cases (empty items, invalid payload)
- Validation errors

**Test Structure:**
- `TestInvoiceCalculatorService`: Unit tests for business logic
- `TestInvoiceAPI`: Integration tests for API endpoints

## Docker

### Build Image

```bash
docker build -t invoice-calculator:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e TOKEN_SECRET="your-secret-token" \
  invoice-calculator:latest
```

## Project Structure

```
microservice-python/
├── application/          # Application services layer
│   ├── mappers.py       # Data mappers
│   └── services.py      # Business service orchestration
├── domain/              # Domain layer
│   ├── model.py         # Domain models (Item, InvoiceCalculationResult)
│   └── rules.py         # Business rules (calculations)
├── infrastructure/      # Infrastructure layer
│   ├── auth.py         # Authentication middleware
│   ├── config.py        # Configuration settings
│   └── fastapi_app.py   # FastAPI app factory
├── presentation/        # Presentation layer
│   └── routes.py        # API routes
├── tests/               # Test suite
│   └── test_calculator.py
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── pytest.ini          # Pytest configuration
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## Dependencies

- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for FastAPI
- **pydantic**: Data validation using Python type annotations
- **pytest**: Testing framework
- **pytest-cov**: Coverage plugin for pytest
- **httpx**: HTTP client (used by TestClient)

## Authentication

The API uses token-based authentication. All endpoints require the `X-API-Token` header with a valid token matching the `TOKEN_SECRET` environment variable.

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
  ```json
  {
    "detail": "Token missing"
  }
  ```
  or
  ```json
  {
    "detail": "Invalid token"
  }
  ```

## Development

### Code Style

- Follows PEP 8 Python style guide
- Uses type hints for better code documentation
- Comprehensive docstrings in English

### Adding New Features

1. **Business Rules**: Add to `domain/rules.py`
2. **Services**: Add to `application/services.py`
3. **API Endpoints**: Add to `presentation/routes.py`
4. **Tests**: Add corresponding tests in `tests/`

## License

[Add your license information here]

