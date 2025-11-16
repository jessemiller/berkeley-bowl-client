# Implementation Plan: Next.js Frontend + Python Backend API

## Project Structure

```
berkeley_bowl_client/
├── backend/
│   ├── __init__.py
│   ├── berkeley_bowl_client.py  (moved from root)
│   ├── api.py                    (FastAPI server)
│   ├── requirements.txt          (backend dependencies)
│   └── .env                      (backend env vars)
│
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── .env.local                (frontend env vars)
│   ├── pages/
│   │   ├── _app.js
│   │   ├── index.js              (login page)
│   │   ├── search.js             (search page)
│   │   └── product/[id].js       (product detail page)
│   ├── components/
│   │   ├── Layout.js
│   │   ├── LoginForm.js
│   │   ├── SearchBar.js
│   │   ├── ProductCard.js
│   │   ├── ProductDetail.js
│   │   └── CartButton.js
│   ├── lib/
│   │   └── api.js                (API client utilities)
│   └── styles/
│       └── globals.css
│
├── README.md                     (updated with full setup)
├── .gitignore                    (updated)
└── PLAN.md                       (this file)
```

## Architecture

### Backend (Python FastAPI)
- **Purpose**: REST API wrapper around `BerkeleyBowlClient`
- **Endpoints**:
  - `POST /api/login` - Authenticate user
  - `GET /api/search?q=...&limit=...` - Search products
  - `GET /api/product/:id` - Get product details
  - `POST /api/cart/add` - Add item to cart
- **Session Management**: Store client sessions in memory (or Redis for production)
- **CORS**: Enable CORS for frontend origin

### Frontend (Next.js)
- **Pages**:
  - `/` - Login page
  - `/search` - Search products
  - `/product/[id]` - Product detail page
- **State Management**: React Context or simple state for auth/session
- **Styling**: Tailwind CSS or simple CSS modules
- **API Client**: Axios or fetch wrapper in `lib/api.js`

## Implementation Steps

1. **Backend Setup**
   - Create `backend/` directory
   - Move `berkeley_bowl_client.py` to `backend/`
   - Create FastAPI server in `backend/api.py`
   - Set up session management (in-memory dict for now)
   - Add CORS middleware
   - Create `backend/requirements.txt` with FastAPI, uvicorn, etc.

2. **Frontend Setup**
   - Create `frontend/` directory
   - Initialize Next.js project
   - Set up Tailwind CSS (or basic CSS)
   - Create API client utilities
   - Set up environment variables

3. **UI Components**
   - Login form component
   - Search page with search bar and results grid
   - Product detail page
   - Add to cart functionality

4. **Integration**
   - Connect frontend to backend API
   - Handle authentication state
   - Error handling and loading states

5. **Documentation**
   - Update README with setup instructions
   - Add development server commands
   - Document API endpoints

## Technology Choices

- **Backend**: FastAPI (modern, fast, auto-docs)
- **Frontend**: Next.js (React framework, great DX)
- **Styling**: Tailwind CSS (utility-first, fast development)
- **HTTP Client**: Axios (frontend), requests (backend)

## Development Workflow

1. Start backend: `cd backend && uvicorn api:app --reload --port 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Backend runs on `http://localhost:8000`
4. Frontend runs on `http://localhost:3000`

## Environment Variables

### Backend (.env)
```
BERKELEY_BOWL_EMAIL=your-email@example.com
BERKELEY_BOWL_PASSWORD=your-password
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Security Considerations

- Backend handles all authentication (credentials never sent to frontend)
- Session tokens stored in backend
- CORS configured for localhost only (development)
- Environment variables for sensitive data

