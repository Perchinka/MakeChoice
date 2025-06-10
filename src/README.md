# `src/`

This is the application’s main source directory. It contains:

- **Configuration & bootstrap**  
  - `config.py`: loads environment variables into a `Settings` object.  
  - `logging.py`: centralizes logger setup.  
  - `main.py`: entry point for running with Uvicorn.

- **Layered application code**  
  - `api/` — HTTP layer (FastAPI routers, Pydantic models).  
  - `domain/` — core domain model (entities, repository interfaces, exceptions, UoW).  
  - `infrastructure/` — database, SSO and repository(I would've call them kind of adapters) implementations.  
  - `services/` — business logic of your app.

Each subdirectory is a “package” that can be swapped or tested in isolation.


