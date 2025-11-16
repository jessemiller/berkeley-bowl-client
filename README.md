# Berkeley Bowl Client

An unofficial Python client and Next.js web interface for interacting with the Berkeley Bowl online ordering system.

## ⚠️ Disclaimer

This is an **unofficial** client library and is not affiliated with or endorsed by Berkeley Bowl. Use at your own risk. The API endpoints used by this library may change at any time without notice.

## Features

- 🔐 User authentication
- 🔍 Product search
- 📦 Product details retrieval
- 🛒 Add items to cart
- 🌐 Modern Next.js web interface

## Project Structure

```
berkeley_bowl_client/
├── backend/              # Python FastAPI server
│   ├── api.py           # FastAPI endpoints
│   ├── berkeley_bowl_client.py  # Core client library
│   └── requirements.txt
├── frontend/            # Next.js application
│   ├── pages/          # Next.js pages
│   ├── components/     # React components
│   └── lib/            # API client utilities
└── berkeley_bowl_client.py  # Standalone client (original)
```

## Quick Start

### Option 1: Web Interface (Recommended)

1. **Set up the backend:**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Create backend `.env` file:**

   ```bash
   cd backend
   cp ../.env.example .env
   # Edit .env with your credentials
   ```

3. **Start the backend server:**

   ```bash
   cd backend
   uvicorn api:app --reload --port 8000
   ```

4. **Set up the frontend (in a new terminal):**

   ```bash
   cd frontend
   npm install
   ```

5. **Create frontend `.env.local` file:**

   ```bash
   cd frontend
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

6. **Start the frontend:**

   ```bash
   cd frontend
   npm run dev
   ```

7. **Open your browser:**

   Navigate to `http://localhost:3000` and login with your Berkeley Bowl credentials.

### Option 2: Python Client Only

If you just want to use the Python client directly:

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
BERKELEY_BOWL_EMAIL=your-email@example.com
BERKELEY_BOWL_PASSWORD=your-password
```

Then use it in your Python code (see [Python Client Usage](#python-client-usage) below).

## Web Interface Usage

The Next.js frontend provides a user-friendly interface to:

1. **Login** - Authenticate with your Berkeley Bowl credentials
2. **Search** - Search for products by name
3. **View Products** - See detailed product information
4. **Add to Cart** - Add items to your shopping cart

### Pages

- `/` - Login page
- `/search` - Product search page
- `/product/[id]` - Product detail page

## Python Client Usage

### Basic Example

```python
from backend.berkeley_bowl_client import BerkeleyBowlClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = BerkeleyBowlClient()

# Login with credentials from environment variables
email = os.getenv("BERKELEY_BOWL_EMAIL")
password = os.getenv("BERKELEY_BOWL_PASSWORD")
client.login(email, password)

# Search for products
results = client.search_products("whole milk", limit=8)
products = results.get("data", {}).get("products", [])

for product in products:
    print(f"{product['title']} - ${product.get('price', 'N/A')}")
```

### Advanced Example

```python
from backend.berkeley_bowl_client import BerkeleyBowlClient
import os
from dotenv import load_dotenv

load_dotenv()

client = BerkeleyBowlClient(
    store_id="2047",  # Default Berkeley Bowl store ID
    timeout=10
)

# Login
client.login(
    os.getenv("BERKELEY_BOWL_EMAIL"),
    os.getenv("BERKELEY_BOWL_PASSWORD")
)

# Search for products
search_results = client.search_products("organic eggs", limit=5)
products = search_results.get("data", {}).get("products", [])

if products:
    # Get details for the first product
    product_id = products[0].get("id")
    product_details = client.get_product(product_id)
    product_data = product_details.get("data", {})
    
    print(f"Product: {product_data.get('title')}")
    print(f"Price: ${product_data.get('price', 'N/A')}")
    
    # Add to cart
    store_product_id = product_data.get("id")
    if store_product_id:
        cart_response = client.add_to_cart(
            store_product_id=store_product_id,
            quantity=2,
            mode="each"
        )
        print("Item added to cart!")
```

## API Reference

### Backend API Endpoints

The FastAPI backend provides the following endpoints:

- `POST /api/login` - Authenticate and get session ID
- `GET /api/search?q=...&limit=...` - Search products
- `GET /api/product/{product_id}` - Get product details
- `POST /api/cart/add` - Add item to cart
- `GET /api/health` - Health check

All endpoints (except login) require the `X-Session-ID` header.

### `BerkeleyBowlClient` (Python)

#### Constructor

```python
BerkeleyBowlClient(
    base_url: str = "https://shop.heinzcatering.berkeleybowl.com",
    store_id: str = "2047",
    timeout: int = 10
)
```

#### Methods

##### `login(email: str, password: str) -> None`

Authenticate with the Berkeley Bowl ordering system.

##### `search_products(query: str, limit: int = 8, mode: str = "pickup") -> Dict[str, Any]`

Search for products in the store.

##### `get_product(product_id: str) -> Dict[str, Any]`

Get detailed information about a specific product.

##### `add_to_cart(store_product_id: str, quantity: int = 1, mode: str = "each") -> Dict[str, Any]`

Add an item to your shopping cart.

## Requirements

### Backend
- Python 3.7+
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `requests` - HTTP library
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

### Frontend
- Node.js 18+
- Next.js 14
- React 18
- Axios - HTTP client
- Tailwind CSS - Styling

## Development

### Running Development Servers

**Backend:**
```bash
cd backend
uvicorn api:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

### Environment Variables

**Backend** (`.env` in `backend/` directory):
```
BERKELEY_BOWL_EMAIL=your-email@example.com
BERKELEY_BOWL_PASSWORD=your-password
```

**Frontend** (`.env.local` in `frontend/` directory):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and personal use.

## Notes

- This client uses the same API endpoints as the official Berkeley Bowl website
- The API may change without notice, which could break this client
- Always use environment variables for credentials - never hardcode them
- The client maintains a session with cookies for authenticated requests
- Backend sessions are stored in-memory (use Redis or a database for production)
