# PataFundi Architecture — Version 1

## Overview

PataFundi is a **Website-First**, **API-First** marketplace connecting customers with technicians in Tanzania.

```
                    PATAFUNDI WEBSITE (React)
                           │
                    REST API (FastAPI)
                           │
                    PostgreSQL + PostGIS
                           │
                         Redis
```

Future Flutter mobile app will consume the **same FastAPI backend**.

## Principles

1. **Website-First** — Professional responsive web UI (not a stretched mobile app).
2. **API-First** — All business logic lives in FastAPI. Frontend is a client.
3. **Certificate-Optional** — Technicians can register and work without any certificate.
4. **Free-First** — No automatic paid services or charges.
5. **Bilingual** — Kiswahili (default) + English.
6. **Themeable** — 5 themes + Light/Dark/System.

## Backend Layers

```
Router → Auth/RBAC → Validation (Pydantic) → Service → Repository → PostgreSQL
```

## Key Models (V1)

- `users` — all roles (CUSTOMER, TECHNICIAN, MERCHANT, AGENCY, ADMIN, SUPER_ADMIN)
- `technician_profiles` — optional certificates, location, ratings
- `certificates` — optional, statuses: PENDING_REVIEW | VERIFIED | REJECTED | EXPIRED
- `service_categories` — Electrician, Plumber, etc.

## Security

- JWT access + refresh tokens
- Bcrypt password hashing
- RBAC via role checks
- CORS restricted
- No secrets in code

## Payment Mode

`PAYMENT_MODE=development` — no real money processed in V1.
