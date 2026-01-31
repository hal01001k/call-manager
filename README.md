# Call Manager

A simple full-stack application to simulated automated voice calls.

## Tech Stack
- **Frontend**: Next.js 16 (React 19), Typescript
- **Backend**: FastAPI (Python 3.12), SQLModel (SQLite)

## Prerequisites
- Node.js (v18.17+)
- Python 3.12+

## Setup & Run

- follow the following step to run it locally with docker

    ```bash
    git clone https://github.com/hal01001k/call-manager.git
    cd call-manager
    sudo docker compose up --build
    ```

### Backend

1. Navigate to the project root.
2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Run the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
   Docs at `http://localhost:8000/docs`.

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies (if not already):
   ```bash
   yarn install
   ```
3. Run the development server:
   ```bash
   yarn dev
   ```
4. Open `http://localhost:3000` in your browser.

## Features
- **Create Call**: Submit a request with Name, Phone, and Workflow.
- **Call List**: View call history and real-time status updates (via polling).
- **Simulation**: The backend simulates a call lifecycle (Pending -> Initiated -> Completed/Failed) using a background task and an internal webhook.

## Technical Architecture & Design Choices

### Core Design Decisions

- **Async/Await Architecture (FastAPI)**
    - **Why:** Utilized `BackgroundTasks` for call initiation and webhook handling.
    - **Benefit:** Prevents API blocking during simulation, allowing handles of high concurrent requests efficiently—essential for telephony applications.
- **Self-Contained Simulation**
    - **Why:** Integrated a mocked provider route (`/provider/send`) directly in the backend.
    - **Benefit:** Eliminates external dependencies (like Twilio) for local development, enabling a zero-setup end-to-end demo.
- **Polling (SWR) over WebSockets**
    - **Why:** Used SWR's `refreshInterval` for automatic UI updates.
    - **Benefit:** Maximizes robustness and simplicity. SWR handles network reconnects, caching, and stale-while-revalidate logic automatically without the state overhead of persistent sockets.
- **Unified Modeling (SQLModel)**
    - **Why:** Leveraged `SQLModel` (Pydantic + SQLAlchemy) for all data structures.
    - **Benefit:** Single Source of Truth for both API validation and database schema, reducing boilerplate and "mapping" bugs.
- **Dockerized Environment**
    - **Why:** Containerized the entire stack with `docker-compose`.
    - **Benefit:** Guarantees consistent network behavior (like the internal webhook loopback) across all development machines.

### Production Roadmap (Future Improvements)

If scaling this system to production, the following upgrades would be prioritized:

| Category | Weakness | Production Fix |
| :--- | :--- | :--- |
| **Reliability** | Background tasks are lost on container restart. | Implement **Redis + Celery** for persistent, retryable task queuing. |
| **UX/Load** | Polling creates constant idle traffic. | Implement **Server-Sent Events (SSE)** for instant, push-based updates. |
| **Storage** | SQLite write-locks during high concurrency. | Migrate to **PostgreSQL** for robust concurrent access and JSONB logging. |
| **Security** | Single static token for all users. | Implement **OAuth2 + JWT** for individual user sessions and private history. |
| **Quality** | Manual verification only. | Add **Pytest** (Backend) and **Playwright** (E2E) for automated CI/CD safety. |