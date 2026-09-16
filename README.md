# Lead Qualifier API

REST API to manage real-estate sales leads and score them automatically using an LLM.

**Live demo:** https://lead-qualifier-api-1kl4.onrender.com/docs
**Repo:** https://github.com/henriquenetoal/lead-qualifier-api

![Tests](https://github.com/henriquenetoal/lead-qualifier-api/actions/workflows/tests.yml/badge.svg)

Heads up: it's hosted on Render's free tier, so it spins down after 15 min idle. First request after that can take 30-50s while it wakes back up.

## Why I built this

I used to work SDR/operations for a land development company (Domus, ~800 lots) and a solar sales company, doing lead tracking in spreadsheets and a CRM. Wanted to build something that actually mirrors that job instead of a random to-do app: leads go through a pipeline, and there's an endpoint that reads the salesperson's raw notes and spits out a score + short summary using an LLM, so someone can tell at a glance which leads are worth calling first.

## What it does

- CRUD for leads (create, list, update status)
- JWT auth, register/login, all lead routes require a token
- `/leads/{id}/qualify` sends the lead's notes to an LLM, gets back a 1-10 score and a summary, saves it on the lead
- pytest tests for auth + protected routes (SQLite locally, real disposable Postgres in CI)
- Dockerized
- GitHub Actions runs the test suite on every push

## Stack

Python, FastAPI, PostgreSQL (SQLAlchemy), JWT (python-jose) + bcrypt, Google Gemini API, pytest, Docker, GitHub Actions, deployed on Render.

## Endpoints

| Method | Route | Auth | What it does |
|---|---|---|---|
| POST | `/register` | no | create account, returns a token |
| POST | `/login` | no | returns a token |
| POST | `/leads` | yes | create a lead |
| GET | `/leads` | yes | list leads |
| PATCH | `/leads/{lead_id}` | yes | update status |
| POST | `/leads/{lead_id}/qualify` | yes | run AI scoring on a lead's notes |

Full docs auto-generated at `/docs` on the live link above.

## About the AI part

Started this with the Anthropic API, then switched to Gemini's free tier because I didn't want to spend money on a portfolio project. Only had to touch `app/ai.py` to do it — nothing else in the app knows or cares which provider is behind `ai.qualify_lead()`.

## Running it locally

```bash
git clone https://github.com/henriquenetoal/lead-qualifier-api.git
cd lead-qualifier-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`.env` file:
```
DATABASE_URL=postgresql://user:password@host/dbname
SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

```bash
uvicorn app.main:app --reload
```

Then go to `http://127.0.0.1:8000/docs`.

## Docker

```bash
docker build -t lead-qualifier-api .
docker run -p 8000:8000 --env-file .env lead-qualifier-api
```

## Tests

```bash
pytest
```

Runs against SQLite in memory locally. CI runs the same tests against a real Postgres container instead, so it's not just testing against a fake DB.

## Still on the list

- Alembic migrations instead of dropping the table every time the schema changes
- `status` as an actual Enum instead of a free string
- Better error handling (duplicate email currently 500s instead of a clean 400)
- Rate limiting on `/qualify`
- Maybe a small React frontend for the pipeline

## Background

3rd semester Systems Analysis and Development at UNIFOR, also doing Mate Academy's Full Stack program. Built this looking for backend/full-stack remote roles in the US market.