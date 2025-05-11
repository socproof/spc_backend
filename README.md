# SimPostCap Backend API

This is the backend API for the SimPostCap project, an application designed for testing ideas and modeling solutions related to post-capitalist scenarios. The API is built with Python, FastAPI, SQLAlchemy, and PostgreSQL, focusing on a microservice-friendly architecture with potential for ML integration.

## Project Goals

The primary goal is to create a robust and scalable backend that can:
1.  Define and manage different "world" scenarios with their inherent problems.
2.  Allow users to define and apply "solutions" to these problems.
3.  Simulate the outcomes of applying these solutions, considering various factors and interdependencies.
4.  Provide a platform for exploring alternatives to current socio-economic models.

## Technologies Used

*   **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Programming Language:** [Python 3.10+](https://www.python.org/)
*   **Database:** [PostgreSQL](https://www.postgresql.org/)
*   **ORM & SQL Toolkit:** [SQLAlchemy](https://www.sqlalchemy.org/) (with async support)
*   **Database Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
*   **Data Validation & Serialization:** [Pydantic](https://pydantic-docs.helpmanual.io/)
*   **Dependency Management:** [Poetry](https://python-poetry.org/)
*   **ASGI Server (for development):** [Uvicorn](https://www.uvicorn.org/)
*   **Containerization (optional, for ease of setup):** Docker (via `docker-compose.yml`)

## Project Structure

```
sim_post_cap_backend/
├── README.md               # This file
├── alembic/                # Alembic migration scripts
├── alembic.ini             # Alembic configuration
├── app/
│   ├── db/                 # Database session, base models
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic schemas for data validation & serialization
│   ├── config.py           # Configuration settings (e.g., database URL from env)
│   └── main.py             # FastAPI application entry point and root routers
├── docker-compose.yml      # Docker Compose for services (e.g., PostgreSQL)
├── poetry.lock             # Poetry lock file for deterministic builds
└── pyproject.toml          # Poetry project configuration and dependencies
```

## Setup and Installation

**Prerequisites:**
*   Python 3.10+
*   Poetry
*   PostgreSQL server (running locally or via Docker)
*   Docker and Docker Compose (if using the provided `docker-compose.yml`)

**1. Clone the Repository (if applicable):**
   ```bash
   git clone https://github.com/socproof/spc_backend.git
   cd spc_backend
   ```

**2. Create and Configure PostgreSQL Database:**
*   Ensure your PostgreSQL server is running.
*   Create a database (e.g., `simpostcap_db`) and a user with appropriate permissions.
*   Update the `DATABASE_URL` in `app/db/session.py` and `alembic.ini` with your actual database credentials and DSN.
    *   *For production, it's highly recommended to use environment variables for these settings.*

**Using Docker Compose for PostgreSQL (Recommended for easy setup):**
A `docker-compose.yml` is provided to quickly set up a PostgreSQL container.
   ```bash
   # Start PostgreSQL service defined in docker-compose.yml
   docker-compose up -d postgres_db
   ```
This will use the default credentials and database name specified in `docker-compose.yml`. Ensure these match your `DATABASE_URL` configuration.

**3. Install Dependencies using Poetry:**
   ```bash
   poetry install
   ```

**4. Activate the Virtual Environment:**
   ```bash
   poetry shell
   ```

**5. Run Database Migrations:**
Make sure you've updated `sqlalchemy.url` in `alembic.ini` and `DATABASE_URL` in `app/db/session.py`.
   ```bash
   alembic upgrade head
   ```
This will create all the necessary tables in your database.

**6. Run the FastAPI Development Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
The API will typically be available at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
*   **Swagger UI:** `http://127.0.0.1:8000/docs`
*   **ReDoc:** `http://127.0.0.1:8000/redoc`

## Running Tests (Setup Pending)

(Test setup with Pytest will be detailed here once implemented.)
```bash
# poetry run pytest
```

## Project Configuration (`app/config.py`)

The `app/config.py` file (or a more robust settings management system) should be used to manage environment variables and application settings, such as:
*   `DATABASE_URL`
*   `API_V1_STR` (API prefix)
*   `PROJECT_NAME`
*   Secret keys, etc.

(This section will be expanded as configuration becomes more complex.)

## How to Contribute

(Details on contributing guidelines, branching strategy, code style, etc., will be added here.)

## Next Steps / Roadmap (High-Level)

*   **Implement CRUD operations** for Worlds, Problem Templates, Solution Templates.
*   Develop the core **Simulation Engine logic**.
*   Create API endpoints for managing `ProblemInstance` and `AppliedSolution` within a world simulation.
*   User authentication and authorization (if required).
*   Integration with a frontend application (e.g., Next.js).
*   Explore and integrate ML components for:
    *   Smart suggestions/recommendations.
    *   Dynamic event generation.
    *   Game balancing.
*   Set up CI/CD pipelines.
*   Comprehensive testing (unit, integration, e2e).

---

*This README is a work in progress and will be updated as the project evolves.*