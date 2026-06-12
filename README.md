# Sorting Game Online

An full-stack online Sorting Algorithm Interactive Game.

## Stack

- Web app: React + TypeScript + Vite
- API: Python FastAPI
- Database: PostgreSQL through SQLAlchemy

## Features

- Register and login
- Passwords stored with PBKDF2 hashes, not plain text or custom ASCII hashes
- Randomized competitive mode
- Bubble sort practice mode
- Insertion sort practice mode
- Browser-based sorting bar UI
- Pass-number questions
- Score saving
- Top 5 leaderboard
- Class and sorting type analytics

## Run loch Docker

```bash
docker compose up --build
```

Then open:

- Web app: http://localhost:5173
- API docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Docker services

```yaml
sorting-game-web
sorting-game-api
sorting-game-db
```

The API connects to PostgreSQL with:

```bash
DATABASE_URL=postgresql://postgres:postgres@sorting-game-db:5432/sorting_game
```

## Run the API manually

Use PostgreSQL locally and set `DATABASE_URL` first.

```bash
cd sorting-game-api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sorting_game
uvicorn app.main:app --reload
```

## Run the web app manually

```bash
cd sorting-game-web
npm install
npm run dev
```

Run normal tests:

```bash
cd sorting-game-api
pytest
```

Run tests with statement:

```bash
pytest --cov=app --cov-branch --cov-report=term-missing
```

The coverage configuration is in `sorting-game-api/pyproject.toml`:

```toml
[tool.coverage.run]
branch = true
source = ["app"]

[tool.coverage.report]
show_missing = true
fail_under = 80
```

## Frontend tests

```bash
cd sorting-game-web
npm install
npm test
```

Included frontend tests:

- `ScorePanel.test.tsx` unit test
- `SortBars.integration.test.tsx` interaction test

## Test types included

### Unit tests

Unit tests check small isolated logic:

- Bubble sort pass generation
- Insertion sort pass generation
- Score calculation
- Password hashing
- Token creation and validation

### Integration tests

- Register user through API
- Login user through API
- Start game through API
- Submit answer through API
- Finish game through API
- Read leaderboard

### Branch coverage

- valid login and invalid login
- valid class and invalid class
- empty score and non-empty score
- sorted arrays and unsorted arrays
- correct and incorrect password verification

## What changed from the original desktop version

The original project used Tkinter, Pygame, local SQLite, and text files for temporary game state. This version, i moved the game rules to the backend and uses a browser frontend. The same idea remains: players identify or construct sorting algorithm passes and earn scores but the project is much more modularised.

## Suggested next improvements

- Replace arrow reorder controls with true drag-and-drop
- Add teacher/admin permissions
- Add timed game enforcement on the backend
- Add analytics charts like a dashboard
- Add Playwright end-to-end tests
- Add Alembic migrations for production database changes

## Screenshots

### Page 1
![Page 1](assets/Mode1.png)

### Page 2
![Page 2](assets/Page2.png)

### Page 3
![Analytics](assets/Analytics.png)

