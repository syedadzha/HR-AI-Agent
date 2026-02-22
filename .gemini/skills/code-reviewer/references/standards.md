# Project Coding Standards

## Backend (FastAPI)
- **Architecture:** Service-oriented. Logic goes in `services/`, routes in `main.py`.
- **Typing:** Strict type hints. Use `typing.Optional`, `list`, `dict` etc.
- **Models:** Use Pydantic `BaseModel` for all data interchange.
- **Logging:** 
    ```python
    from logger_config import logger
    logger.info("Informational message", extra={"key": "value"})
    logger.error("Error occurred", exc_info=True)
    ```
- **Async:** Use `async def` for I/O bound operations (database, vector search).

## Frontend (Nuxt 3)
- **Styling:** Vanilla CSS + Tailwind CSS. Avoid Tailwind for complex components if it gets messy.
- **Components:** Functional components in `components/`.
- **State:** Pinia for global state.
- **Types:** TypeScript `interface` or `type` for all data structures.

## Documentation
- Maintain `GEMINI.md` as the source of truth for architecture and tech stack.
- Update `README.md` for setup instructions.

## Testing
- Pytest for backend.
- Place tests in `backend/tests/`.
- Use descriptive test names.
