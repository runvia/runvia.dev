# runvia.dev

> My personal portfolio and CV site, built from scratch as both a showcase and a learning project.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Build Status](https://github.com/runvia/runvia.dev/actions/workflows/ci.yml/badge.svg)](https://github.com/runvia/runvia.dev/actions)
[![Deploy Status](https://github.com/runvia/runvia.dev/actions/workflows/deploy.yml/badge.svg)](https://github.com/runvia/runvia.dev/actions)

**Live:** https://runvia.dev

---

## About

This repository contains everything behind [runvia.dev](https://runvia.dev): a React frontend, a FastAPI backend with a PostgreSQL database, and the Docker and Traefik setup that runs it on a DigitalOcean droplet.

The site shows my CV and the projects I've worked on. Small browser games are planned next (see [`future_projects.md`](future_projects.md)).

It's also deliberately a learning project. I'm using it to get hands-on with a modern web stack end to end: frontend, API, database, infrastructure, CI and operations.

## Tech stack

| Area | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS 3, React Router 7, served by nginx |
| Backend | FastAPI (Python 3.13), SQLModel, Alembic migrations, PostgreSQL 16 |
| Content editing | SQLAdmin, restricted to active superusers |
| Infrastructure | Docker Compose with `dev` and `prod` profiles, Traefik v3 with Let's Encrypt (DNS-01) |
| Hosting | DigitalOcean droplet, nightly database backups to Cloudflare R2 |
| Quality | GitHub Actions (ESLint, TypeScript build, ruff, pytest), pre-commit hooks |

## Architecture

```mermaid
flowchart LR
    browser([Browser]) -->|HTTPS| traefik[Traefik]
    traefik -->|"/"| nginx["nginx<br/>(React build)"]
    traefik -->|"/api, /admin"| api["FastAPI<br/>+ SQLAdmin"]
    api --> db[(PostgreSQL)]
```

Traefik is the only public entry point. It terminates TLS, redirects HTTP to HTTPS, adds security headers, and routes each request either to nginx, which serves the built React app, or to FastAPI, which serves the JSON API and the admin interface.

The [`architecture/`](architecture) folder documents the design of the site following the TOGAF Architecture Development Method. There's one folder per phase, from [`01_Preliminary`](architecture/01_Preliminary) to [`08_ChangeManagement`](architecture/08_ChangeManagement), with the diagrams in [`architecture/diagrams`](architecture/diagrams).

## Running locally

### Prerequisites

- Docker with Docker Compose
- To work on the code outside the containers: Node.js 22, Python 3.13 and [uv](https://docs.astral.sh/uv/)

### 1. Create a `.env` file

Create `.env` in the repository root, next to `docker-compose.yaml`. It needs these variables:

```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
DATABASE_URL=
ADMIN_USERNAME=
ADMIN_PASSWORD=
SECRET_KEY=
SESSION_SECRET_KEY=
DATABASE_ECHO=false
```

- `DATABASE_URL` points at the Compose service, so its host is `postgres`: `postgresql://USER:PASSWORD@postgres:5432/DB`.
- `SECRET_KEY` and `SESSION_SECRET_KEY` must each be at least 32 characters. Generate them with `openssl rand -base64 32`.
- `ADMIN_USERNAME` and `ADMIN_PASSWORD` create the first admin user on startup.

[Section 9 of the runbook](docs/runbook.md#9-create-the-env-file) explains each variable in detail, including the production-only `DO_AUTH_TOKEN`.

### 2. Start the stack

```bash
docker compose --profile dev up --build
```

Database migrations run automatically when the backend starts.

| URL | What |
|---|---|
| http://localhost | The site |
| http://localhost/api/docs | Interactive API documentation |
| http://localhost/admin/ | SQLAdmin, to edit the CV content |
| http://localhost:8080 | Traefik dashboard |

PostgreSQL is also reachable from the host on port `55432`.

### 3. Development tools

Install the dependencies locally, so your editor can see them and you can run the checks:

```bash
cd backend && uv sync
```

```bash
cd frontend && npm ci
```

`npm ci` installs exactly what `package-lock.json` specifies. `npm install` can rewrite the lockfile, so only use it when you mean to change dependencies.

Then install the git hooks, which run ruff and pytest before every commit:

```bash
uv tool install pre-commit
pre-commit install
```

### Tests and linting

```bash
uv run --directory backend pytest
```

```bash
cd frontend && npm run lint && npm run build
```

The backend tests use an in-memory SQLite database, so they don't need Docker or a running PostgreSQL. CI runs the same checks on every pull request.

## Project structure

```
runvia.dev/
├─ frontend/              React app
│  ├─ src/
│  │  ├─ pages/           one component per route
│  │  ├─ components/      shared layout and route guards
│  │  ├─ api/             API client
│  │  └─ context/         authentication state
│  ├─ nginx/              nginx config for the production image
│  └─ Dockerfile
├─ backend/               FastAPI app
│  ├─ app/
│  │  ├─ routers/         API endpoints
│  │  ├─ models/          database tables (SQLModel)
│  │  └─ schemas/         API response shapes
│  ├─ alembic/            database migrations
│  ├─ tests/
│  └─ Dockerfile
├─ architecture/          TOGAF architecture documentation
├─ docs/
│  └─ runbook.md          deployment and operations runbook
├─ .github/workflows/     CI
└─ docker-compose.yaml    dev and prod stacks
```

## Deployment

The site runs on a single DigitalOcean droplet using the `prod` Compose profile. The [runbook](docs/runbook.md) covers everything from creating the droplet to restoring and backing up the database.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- Email: [contact@runvia.dev](mailto:contact@runvia.dev)
- GitHub: [runvia](https://github.com/runvia)
