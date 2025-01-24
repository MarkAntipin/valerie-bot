# Dynamic Settings Service


**Dependencies:**

- python >= 3.12
- poetry
- postgres + pgvector (for ex in Docker https://hub.docker.com/r/pgvector/pgvector)
- golang-migrate (https://github.com/golang-migrate/migrate)

**Create .env with: (look at [.env.example](.env.example))**
```
PG_HOST=localhost
PG_PORT=5437
PG_USER=valerie
PG_PASSWORD=valerie
PG_DATABASE=valerie

TOKEN=
OPENAI_KEY=
```

**Install libs:**
```
poetry install
```

**Run postgres with docker:**
```
docker run --name valerie -e POSTGRES_USER=valerie -e POSTGRES_PASSWORD=valerie -e POSTGRES_DB=valerie -p 5437:5432 -d pgvector/pgvector:pg17
```

**Apply migrations:**
```
migrate -path migrations -database "postgres://valerie:valerie@localhost:5437/valerie?sslmode=disable" up
```

**Run bot:**
```
poetry run python run_bot.py
```

**Create migration:**
```
migrate create -ext sql -dir migrations {migration-name} 
```

### Linter:
```
poetry run ruff check . --fix
```