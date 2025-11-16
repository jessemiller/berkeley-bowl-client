from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from berkeley_bowl_client import BerkeleyBowlClient

app = FastAPI(title="Berkeley Bowl API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (use Redis or database in production)
sessions: Dict[str, BerkeleyBowlClient] = {}


# Request/Response models
class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    session_id: str
    message: str


class AddToCartRequest(BaseModel):
    store_product_id: str
    quantity: int = 1
    mode: str = "each"


@app.post("/api/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Authenticate user and create a session"""
    try:
        client = BerkeleyBowlClient()
        client.login(credentials.email, credentials.password)
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        sessions[session_id] = client
        
        return LoginResponse(
            session_id=session_id,
            message="Login successful"
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")


def get_client(session_id: str) -> BerkeleyBowlClient:
    """Get client instance from session"""
    if session_id not in sessions:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return sessions[session_id]


@app.get("/api/search")
async def search(
    q: str,
    limit: int = 8,
    mode: str = "pickup",
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Search for products"""
    if not x_session_id:
        raise HTTPException(status_code=401, detail="Session ID required")
    
    try:
        client = get_client(x_session_id)
        results = client.search_products(query=q, limit=limit, mode=mode)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/api/product/{product_id}")
async def get_product(
    product_id: str,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Get product details"""
    if not x_session_id:
        raise HTTPException(status_code=401, detail="Session ID required")
    
    try:
        client = get_client(x_session_id)
        product = client.get_product(product_id).get("data")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get product: {str(e)}")


@app.post("/api/cart/add")
async def add_to_cart(
    request: AddToCartRequest,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Add item to cart"""
    if not x_session_id:
        raise HTTPException(status_code=401, detail="Session ID required")
    
    try:
        client = get_client(x_session_id)
        result = client.add_to_cart(
            store_product_id=request.store_product_id,
            quantity=request.quantity,
            mode=request.mode
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add to cart: {str(e)}")


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

