# runvia.dev

> A personal portfolio and CV site showcasing my projects and skills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
[![Build Status](https://github.com/runvia/runvia.dev/actions/workflows/ci.yml/badge.svg)](https://github.com/runvia/runvia.dev/actions)  
[![Deploy Status](https://github.com/runvia/runvia.dev/actions/workflows/deploy.yml/badge.svg)](https://github.com/runvia/runvia.dev/actions)


---

## Table of Contents

1. [About](#about)
2. [Demo](#demo)
3. [Tech Stack](#tech-stack)  
4. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running Locally](#running-locally)
5. [Project Structure](#project-structure)  
6. [Usage](#usage)  
7. [Contributing](#contributing)  
8. [Changelog](#changelog)  
9. [License](#license)  
10. [Contact](#contact)


---

## About

_This repo contains the source code for my personal website, runvia.dev—a React frontend with a FastAPI backend, containerized with Docker & Traefik. You’ll find my CV, project showcases, and a blog to share what I’m learning._

---

## Demo

_runvia.dev(https://runvia.dev)_

![Home page screenshot](./assets/screenshots.png)

---

## Tech Stack

- **Frontend**: React (CRA, hooks)  
- **Backend**: FastAPI, Uvicorn  
- **Containerization**: Docker, Docker Compose + Traefik  
- **CI/CD**: GitHub Actions
- **Hosting**: DigitalOcean (pick one)

---

## Getting Started

### Prerequisites

- Node.js ≥14.x & npm  
- Python ≥3.9 & pip  
- Docker & Docker Compose  
- VS Code (with ESLint, Prettier, Python, Docker extensions)

### Installation

1. **Clone** the repo  
```bash
git clone https://github.com/runvia/runvia.dev.git
cd runvia.dev
```
2. **Install frontend deps**
```bash
cd frontend
npm install
```
3. **Install backend deps**
```bash
cd ../backend
pip install -r requirements.txt
```

### Running Locally

In the project root
```bash
docker-compose up --build
```

 - Frontend --> http://localhost
 - API --> http://api.localhost/docs 

---

## Project Structure

```bash
runvia.dev/
├─ frontend/        # React app (CRA)
│  ├─ src/
│  │  ├─ components/
│  │  ├─ pages/
│  │  └─ assets/
│  └─ Dockerfile
├─ backend/         # FastAPI
│  ├─ app/
│  │  ├─ routers/
│  │  └─ models/
│  └─ Dockerfile
├─ docker-compose.yml
├─ .github/         # workflows, issue/PR templates
├─ .gitignore
├─ README.md
└─ LICENSE
```

---

## Usage

Explain how to:

 - Add a new page in react
 - Expose a new endpoint in FastAPI
 - Write documentation in /docs (if you have any)
 - Update the Docker Compose labels for Traefik routing

 ---

 ## Contributing

 1. Fork the repo
 2. Create a branch: feature/my-new-app
 3. Commit your changes with a clear message
 4. Open a PR against develop
 5. Ensure linting passes & docs are updated

---

## Changelog

### [unreleased]
- ✨ Add Blog page skeleton
- 🐛 Fix header nav link styling

### [v0.1.0] – 2025-04-23
- Initial scaffold: React + FastAPI + Docker + Traefik

---

## License

This project is licensed under the MIT License

## Contact 
- Runvia
- Email: [contact@runvia.dev](mailto:contact@runvia.dev)
- Github: Runvia