# Application & Data Architecture – runvia.dev

This ArchiMate view defines the key application components, interfaces, and data objects that support the capabilities and use cases of runvia.dev. It illustrates how frontend and backend components are structured, how they interact with clients, and how data flows through the system.

---

## 📦 Application Components

| Component                | Description                                                                          |
|--------------------------|--------------------------------------------------------------------------------------|
| **React Frontend**       | Web application that renders UI, routes client views, and consumes API data          |
| **FastAPI Backend**      | REST API server that serves project data, CV documents, and handles contact messages |
| **Web UI (Interface)**   | Application interface exposed to users via the browser                               |
| **REST API (Interface)** | Programmatic interface exposed by the backend                                        |
| **Traefik Proxy**        | Reverse proxy handling HTTPS routing to the frontend and backend                     |

---

## 💾 Data Objects

| Data Object          | Description                                                             |
|----------------------|-------------------------------------------------------------------------|
| **Project Metadata** | JSON or markdown-based project descriptions shown in the frontend       |
| **CV Document**      | PDF or structured data representing the user's CV                       |
| **Contact Messages** | Form submissions sent via the contact page (may go to email or storage) |

---

## 🧱 Technology Layer

- **Client Browser** (external user device accessing the site via HTTPS)
- **Traefik Proxy** routes requests internally via HTTP
- Future extensions may include:
  - `Docker Compose` as system software
  - `GitHub Actions` as artifact or automation component

---

## 🗺️ Relationships

- `Client Browser` uses the `Web UI`
- `Web UI` is **realized by** the `React Frontend`
- `React Frontend` **calls** the `REST API`
- `REST API` is **realized by** the `FastAPI Backend`
- `FastAPI Backend` **reads/writes** `Project Metadata`, `CV Document`, and `Contact Messages`

---

## 🗂 Diagram Location

- File: `architecture/04_InformationSystems/App & Data Architecture.drawio`
- View type: ArchiMate Application & Data Layer

---

## 🔗 Linked Views

- Related to use cases in: `03 - Use Case Diagram`
- Realizes capabilities in: `02 - Capabilities`

---

