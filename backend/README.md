# Berkeley Bowl Backend API

FastAPI server that wraps the Berkeley Bowl client library.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your credentials:
   ```
   BERKELEY_BOWL_EMAIL=your-email@example.com
   BERKELEY_BOWL_PASSWORD=your-password
   ```

3. Run the server:
   ```bash
   uvicorn api:app --reload --port 8000
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

- `POST /api/login` - Authenticate and get session ID
- `GET /api/search?q=...&limit=...` - Search products (requires X-Session-ID header)
- `GET /api/product/{product_id}` - Get product details (requires X-Session-ID header)
- `POST /api/cart/add` - Add item to cart (requires X-Session-ID header)
- `GET /api/health` - Health check

