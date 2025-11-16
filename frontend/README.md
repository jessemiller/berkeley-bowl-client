# Berkeley Bowl Frontend

Next.js web interface for the Berkeley Bowl client.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env.local` file:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Make sure the backend server is running (see `../backend/README.md`)

4. Run the development server:
   ```bash
   npm run dev
   ```

The app will be available at `http://localhost:3000`

## Pages

- `/` - Login page
- `/search` - Product search
- `/product/[id]` - Product detail page

## Build for Production

```bash
npm run build
npm start
```

