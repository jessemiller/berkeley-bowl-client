# Berkeley Bowl Client

An unofficial Python client for interacting with the Berkeley Bowl online ordering system.

## ⚠️ Disclaimer

This is an **unofficial** client library and is not affiliated with or endorsed by Berkeley Bowl. Use at your own risk. The API endpoints used by this library may change at any time without notice.

## Features

- 🔐 User authentication
- 🔍 Product search
- 📦 Product details retrieval
- 🛒 Add items to cart

## Installation

```bash
pip install -r requirements.txt
```

Or install dependencies directly:

```bash
pip install requests python-dotenv
```

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd berkeley_bowl_client
   ```

2. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Berkeley Bowl credentials:
   ```
   BERKELEY_BOWL_EMAIL=your-email@example.com
   BERKELEY_BOWL_PASSWORD=your-password
   ```

   **Important:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

### Basic Example

```python
from berkeley_bowl_client import BerkeleyBowlClient
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
from berkeley_bowl_client import BerkeleyBowlClient
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

### `BerkeleyBowlClient`

#### Constructor

```python
BerkeleyBowlClient(
    base_url: str = "https://shop.heinzcatering.berkeleybowl.com",
    store_id: str = "2047",
    timeout: int = 10
)
```

- `base_url`: Base URL for the Berkeley Bowl API (default: production URL)
- `store_id`: Store ID to use (default: "2047")
- `timeout`: Request timeout in seconds (default: 10)

#### Methods

##### `login(email: str, password: str) -> None`

Authenticate with the Berkeley Bowl ordering system.

**Parameters:**
- `email`: Your Berkeley Bowl account email
- `password`: Your Berkeley Bowl account password

**Raises:**
- `requests.HTTPError`: If authentication fails

##### `search_products(query: str, limit: int = 8, mode: str = "pickup") -> Dict[str, Any]`

Search for products in the store.

**Parameters:**
- `query`: Search query string
- `limit`: Maximum number of results to return (default: 8)
- `mode`: Order mode, typically "pickup" (default: "pickup")

**Returns:**
- Dictionary containing search results with product data

##### `get_product(product_id: str) -> Dict[str, Any]`

Get detailed information about a specific product.

**Parameters:**
- `product_id`: The product ID to retrieve

**Returns:**
- Dictionary containing detailed product information

##### `add_to_cart(store_product_id: str, quantity: int = 1, mode: str = "each") -> Dict[str, Any]`

Add an item to your shopping cart.

**Parameters:**
- `store_product_id`: The store-specific product ID
- `quantity`: Quantity to add (default: 1)
- `mode`: Pricing mode, typically "each" (default: "each")

**Returns:**
- Dictionary containing updated cart information

## Requirements

- Python 3.7+
- `requests` - HTTP library
- `python-dotenv` - Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and personal use.

## Notes

- This client uses the same API endpoints as the official Berkeley Bowl website
- The API may change without notice, which could break this client
- Always use environment variables for credentials - never hardcode them
- The client maintains a session with cookies for authenticated requests

