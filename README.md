# PataFundi — Version 1 (Website Foundation)

**Pata Fundi Sahihi, Kwa Wakati Sahihi.**  
Find the Right Technician, at the Right Time.

Tanzanian Technician & Services Marketplace  
**Website-First • API-First • Free-First • Certificate-Optional • Bilingual • 5 Themes**

---

## Version Roadmap

| Version | Focus |
|---------|-------|
| **V1 (This)** | Project foundation, Auth, RBAC, Themes, Language, Settings, Responsive UI, Technician registration (certs optional), Admin skeleton |
| **V2** | Full technician profiles, Search & filters, Bookings, Job lifecycle, Customer & Technician dashboards |
| **V3** | Trust system, Chat, Notifications, Payments/Escrow (dev mode), Spare parts marketplace, Advanced admin |

---

## Tech Stack (V1)

**Frontend**
- React 18 + TypeScript + Vite
- Tailwind CSS
- React Router
- Axios + TanStack Query
- Lucide React icons
- i18n (Kiswahili default + English)
- 5 Themes + Light/Dark/System

**Backend**
- Python 3.11+ / FastAPI
- SQLAlchemy + Alembic
- PostgreSQL (+ PostGIS ready)
- JWT Authentication
- RBAC
- Pydantic

**Infrastructure**
- Docker Compose (frontend, backend, postgres, redis)
- Redis (ready for later caching/queues)

---

## Quick Start (Local Development)

### Option A — Docker (Recommended)

```bash
cd patafundi
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Option B — Manual

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env if needed (defaults work with Docker Postgres)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

## Critical Business Rules (Already Implemented)

- Certificates are **OPTIONAL**. Technicians can register and work without any certificate.
- Verified certificates only add a trust badge — they never block registration or ranking.
- Free-first: no automatic paid services, no automatic charging.
- Website-first: this is a professional responsive web app (not a stretched mobile UI).
- API-first: same FastAPI backend will power a future Flutter app.

---

## Project Structure

```
patafundi/
├── frontend/          # React + TypeScript + Vite + Tailwind
├── backend/           # FastAPI + SQLAlchemy
├── docs/              # Architecture, API, Security docs
├── infrastructure/    # Future infra configs
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Default Seed Accounts (Development)

| Role       | Email / Phone          | Password   |
|------------|------------------------|------------|
| Super Admin| admin@patafundi.co.tz  | Admin@123  |
| Customer   | customer@example.com   | Customer1! |
| Technician | fundi@example.com      | Fundi123!  |

(Phone verification & real OTP will be added in later versions.)

---

## Language & Themes

- Default language: **Kiswahili**
- Switch anytime in Settings → Language
- Themes: PataFundi Classic • Ocean • Forest • Sunset • Midnight
- Appearance: Light / Dark / System

---

## Next Steps (Version 2)

After you run and explore V1, we will add:
- Full technician search with PostGIS distance
- Booking flow & job status machine
- Customer & Technician dashboards
- Real-time readiness (WebSockets skeleton)

---

Built with ❤️ for Tanzania.  
PataFundi — Find the Right Technician, at the Right Time.
