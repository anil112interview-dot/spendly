# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Common Development Commands

| Task | Command | Notes |
|------|---------|-------|
| **Create a virtual environment** | `python -m venv venv` | Windows; activates an isolated Python environment. |
| **Activate the virtual environment** | `.\venv\Scripts\activate` | PowerShell; use `deactivate` to exit. |
| **Install dependencies** | `pip install -r requirements.txt` | Installs Flask, pytest, and related packages. |
| **Run the application (development server)** | `python app.py` | Starts Flask on `http://127.0.0.1:5001` with `debug=True`. |
| **Run all tests** | `pytest` | Discovers any `test_*.py` files under the repo. |
| **Run a single test file** | `pytest tests/test_xyz.py` | Replace `tests/test_xyz.py` with the desired path. |
| **Run a single test function** | `pytest -k test_name` | Use a substring that uniquely matches the target test. |
| **Lint (if a linter is added)** | `flake8 .` | Recommended if a linting tool is introduced later. |
| **Database initialization (once)** | `python -c "from database.db import init_db, seed_db; init_db(); seed_db()"` | Creates tables and seeds sample data for local development. |
| **Reset the database** | Delete `instance/*.sqlite` (if using a file‑based DB) and re‑run the init command above. | Adjust path if the DB location changes. |

> **Tip:** After installing the virtual environment, keep the terminal inside `C:\Tutorials\claude\expense-tracker` so relative paths work as expected.

---

## High‑Level Architecture Overview

- **`app.py`** – The Flask entry point.
  - Instantiates the `Flask` app.
  - Declares top‑level routes (`/`, `/register`, `/login`, `/terms`, `/privacy`) that render Jinja2 templates from the **`templates/`** folder.
  - Contains placeholder routes (`/logout`, `/profile`, `/expenses/*`) that will be fleshed out in later steps (e.g., authentication, CRUD for expenses).
  - Runs the server with `app.run(debug=True, port=5001)` when executed directly.

- **Templates (`templates/*.html`)** – Jinja2 files extending a base layout (`base.html`).
  - Provide the UI for landing page, registration, login, and static informational pages.
  - Use Flask’s `url_for` to reference routes, making URL changes safe.

- **Static Assets (`static/css/`, `static/js/`)** – Client‑side styling and behavior.
  - `style.css` defines the visual theme used across templates.
  - `main.js` is intended for interactive front‑end logic (currently empty).

- **Database Layer (`database/`)** – Planned SQLite helper.
  - `db.py` (currently a stub) will expose:
    - `get_db()` – Returns a SQLite connection with `row_factory` and foreign‑key enforcement.
    - `init_db()` – Executes `CREATE TABLE IF NOT EXISTS` statements for all tables.
    - `seed_db()` – Inserts sample data useful for local development and testing.
  - `__init__.py` makes the folder a package, allowing imports like `from database.db import get_db`.

- **Testing (`requirements.txt` includes `pytest` & `pytest‑flask`)** –
  - Tests should live under a `tests/` directory (e.g., `tests/test_routes.py`).
  - Use `pytest-flask` fixtures (`client`, `app`) to issue requests against the Flask app without launching a server.
  - Example test pattern:
    ```python
    def test_landing_page(client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"Spendly" in resp.data
    ```

- **Configuration & Environment** –
  - The project does not currently use a `.env` file; any secret keys (e.g., Flask `SECRET_KEY`) should be added there and loaded via `python-dotenv` if needed.
  - All dependencies are pinned in `requirements.txt` to ensure reproducible environments.

- **Development Flow (Typical)**
  1. **Setup** – Create and activate a virtual environment, install dependencies.
  2. **Database** – Run the init/seed command to create a fresh SQLite file.
  3. **Implement Features** – Add route handlers, forms, and DB queries in the placeholder sections of `app.py`.
  4. **Write Tests** – Create/extend `tests/` to cover new routes and business logic.
  5. **Run Tests** – `pytest` ensures regressions are caught early.
  6. **Run App** – `python app.py` to see UI changes in a browser at `http://127.0.0.1:5001`.

---

## Project‑Specific Rules & Guidance

- No Cursor or Copilot rule files (`.cursor/` or `.github/copilot-instructions.md`) are present, so no special directives need to be enforced.
- The repository’s `README.md` is minimal; the most relevant content is the app’s purpose and the placeholder steps indicated by comments in `app.py` and `database/db.py`.
- Keep code style consistent with existing files (e.g., two‑space indentation, descriptive comment blocks before logical sections).

---

## Suggested Future Enhancements for CLAUDE.md

- If a `.cursor/rules/` directory is added, summarize any “must‑include” or “must‑avoid” directives here.
- When more scripts (e.g., a CLI management command) are added, extend the **Common Development Commands** table with those commands.
- As testing grows, consider adding a section describing test organization (unit vs. integration) and any custom pytest fixtures.

---

*End of CLAUDE.md*