import os
import requests
import base64
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class BerkeleyBowlClient:
    def __init__(
        self,
        base_url: str = "https://shop.heinzcatering.berkeleybowl.com",
        store_id: str = "2047",
        timeout: int = 10,
    ):
        self.base_url = base_url.rstrip("/")
        self.store_id = store_id
        self.timeout = timeout

        self.session = requests.Session()
        # Pretend to be a normal browser
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/142.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/",
            }
        )

    # ---------- AUTH ----------

    def login(self, email: str, password: str) -> None:
        """
        Log in using the same endpoint as your curl:
        POST /rest-proxy/v2/auth/login
        """
        url = f"{self.base_url}/rest-proxy/v2/auth/login"
        payload = {
            "type": "email",
            "email": email,
            "password": password,
        }

        resp = self.session.post(url, json=payload, timeout=self.timeout)
        print("Login status:", resp.status_code)
        #print("Login response text:", resp.text[:500])
        resp.raise_for_status()

        #print("Cookies after login:", self.session.cookies.get_dict())

    # ---------- PRODUCT ----------
    def search_products(
        self,
        query: str,
        limit: int = 8,
        mode: str = "pickup",
    ):
        """
        Search products, matching your curl:

        POST /rest-proxy/v2/layout/stores/{store_id}/products/search?mode=...&limit=...

        `eSearch` is the base64-encoded search term.
        """
        url = f"{self.base_url}/rest-proxy/v2/layout/stores/{self.store_id}/products/search"

        params = {
            "mode": mode,
            "limit": str(limit),
        }

        encoded_query = base64.b64encode(query.encode("utf-8")).decode("ascii")

        payload = {
            "tagId": [],
            "categoryId": None,
            "departmentId": None,
            "eSearch": encoded_query,
        }

        resp = self.session.post(
            url,
            params=params,
            json=payload,
            timeout=self.timeout,
        )
        print("search_products status:", resp.status_code)
        print("search_products response snippet:", resp.text[:5000])
        resp.raise_for_status()
        return resp.json()

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Fetch product details, now relying only on the authenticated session.
        """
        url = f"{self.base_url}/rest-proxy/v2/layout/stores/{self.store_id}/products/{product_id}"
        params = {"mode": "pickup"}

        resp = self.session.get(url, params=params, timeout=self.timeout)
        print("get_product status:", resp.status_code)
        resp.raise_for_status()
        return resp.json()

    # ---------- CART ----------

    def add_to_cart(
        self,
        store_product_id: str,
        quantity: int = 1,
        mode: str = "each",
    ) -> Dict[str, Any]:
        """
        Add an item to cart, matching your curl:

        PUT /rest-proxy/v2/layout/cart/add
          ?productExpands=...
          &expand=...
        """
        url = f"{self.base_url}/rest-proxy/v2/layout/cart/add"

        params = {
            "productExpands": (
                "is_in_default_favorite_list,modifications,"
                "availableModifications,modificationsAttributes,store_mapping"
            ),
            "expand": "loyalty,withOutOfStockProducts",
        }

        payload = {
            "mode": mode,
            "quantity": quantity,
            "storeProductId": str(store_product_id),
            "modificationId": None,
        }

        resp = self.session.put(
            url,
            params=params,
            json=payload,
            timeout=self.timeout,
        )
        print("add_to_cart status:", resp.status_code)
        #print("add_to_cart response text:", resp.text[:500])
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    client = BerkeleyBowlClient()

    EMAIL = os.getenv("BERKELEY_BOWL_EMAIL")
    PASSWORD = os.getenv("BERKELEY_BOWL_PASSWORD")

    if not EMAIL or not PASSWORD:
        raise ValueError(
            "Please set BERKELEY_BOWL_EMAIL and BERKELEY_BOWL_PASSWORD environment variables"
        )

    client.login(EMAIL, PASSWORD)

    results = client.search_products("whole milk", limit=8).get("data")
    #print("Search keys:", results.keys())
    print("First item:", results["products"][0]["title"] if "products" in results and results["products"] else None)
    
    # 1) Get product details so we can see storeProductId
    product = client.get_product("2142896100").get("data")
    print("Product name:", product.get("title"))

    store_product_id = product.get("id")
    print("store_product_id:", store_product_id)

    if store_product_id:
        cart = client.add_to_cart(store_product_id, quantity=1, mode="each")
        print("Cart response keys:", cart.keys())
    else:
        print("Could not find store_product_id in product JSON – print(product) and inspect.")
