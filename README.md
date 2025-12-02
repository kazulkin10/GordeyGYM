# Gordey GYM Admin

Production-ready admin web application for Gordey GYM front-desk teams. Backend built with FastAPI and PostgreSQL; frontend built with React + Vite + MUI. Docker images and docker-compose simplify local development and deployment.

## Architecture
- **Backend** (`backend/`): FastAPI + SQLAlchemy, token auth (JWT), role support, health check, visits logic, migrations via SQL scripts.
- **Frontend** (`frontend/`): React SPA with MUI, sidebar layout, screens for dashboard, clients, subscription types, and visit scanning.
- **Database**: PostgreSQL with schema in `backend/migrations/001_init.sql`.
- **Containers**: `docker-compose.yml` wires DB, API, and SPA.

### Data Model Highlights
- Users with roles (`admin`, `manager`, `operator`).
- Clients with unique barcodes, contact data, balance, notes, VIP flag.
- Subscription types (price, duration, visit count), subscriptions with status tracking and payment metadata.
- Visits with direction (in/out) from barcode scans and double-scan protection.

## Running locally
```bash
docker-compose up --build
```
API: http://localhost:8000
Frontend: http://localhost:5173

Configure environment via `.env` (backend reads `DATABASE_URL`, `SECRET_KEY`, etc.). Default compose uses local Postgres.

## Backend
- Entrypoint: `backend/app/main.py`
- Auth token endpoint: `POST /api/auth/token` (OAuth2 password flow)
- Health check: `GET /health`
- Core routes: clients, subscriptions, visits (scan endpoint enforces active subscription and double-scan guard)
- Tests: `pytest` inside `backend/`

Run tests:
```bash
cd backend
pip install -r requirements.txt
pytest
```

## Frontend
- Vite dev server: `npm install && npm run dev` inside `frontend/`
- API base configured via `VITE_API_URL` (defaults to `http://localhost:8000`)
- Modern layout with sidebar navigation and dialogs for quick creation flows.

## Deployment notes
- Build images via Dockerfiles in `backend/` and `frontend/`.
- Serve backend behind reverse proxy (TLS termination) and point frontend to the API host.
- Apply migrations from `backend/migrations` to production database before deploying new versions.
