# Solutions Overview – runvia.dev

This document outlines the high-level solution building blocks (SBBs) identified in Phase 5 of the TOGAF ADM. These solutions map to the previously defined capabilities and support implementation planning and deployment alignment.

Each solution groups technical components, interfaces, and logic into deployable units.

---

## 🧩 Solution 1: Frontend

**Purpose**: Provide the user interface for visitors to explore projects, view the CV, and interact with the contact form.

**Includes**:
- `React Frontend`: Main UI logic and routing
- `Web UI`: Application interface used by the browser

**Realizes Capabilities**:
- Personal Branding
- Project Showcase
- Communication (UI side)

---

## 🧩 Solution 2: Backend API

**Purpose**: Deliver project and personal data, and handle user contact messages securely via a REST API.

**Includes**:
- `FastAPI Backend`: Handles HTTP requests, serialization, logic
- `REST API`: Interface for frontend and external services
- `Contact Message Logic`: Receives and processes form input

**Realizes Capabilities**:
- Project Showcase
- Contact Integration
- Share Codebase (indirectly via GitHub data)

---

## 🧩 Solution 3: DevOps & Infrastructure

**Purpose**: Support deployment, reverse proxy routing, and future CI/CD automation.

**Includes**:
- `Traefik Proxy`: Handles HTTPS, routing between frontend and backend
- `Docker Compose`: Local orchestration for all services
- `GitHub Actions`: CI/CD workflows (planned) for building, testing, and deploying changes

**Supports**:
- Automation by Design (Principle)
- Modular Structure
- Self-managed Infrastructure

---

## 📂 Diagram File

- Located at: `architecture/05_OpportunitiesAndSolutions/Solutions Overview.drawio`

## 🔗 Related Artifacts

- Capabilities defined in: `02 - Capabilities.drawio`
- Use cases defined in: `03 - Use Case Diagram.drawio`
- App and data architecture in: `04 - App & Data Architecture.drawio`

---

