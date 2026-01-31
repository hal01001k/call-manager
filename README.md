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

