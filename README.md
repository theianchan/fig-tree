# fig-tree

To install on a new machine:
- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `brew install postgresql`
- `brew services start postgresql`
- `createdb tree`
- `touch .env`

`.env` needs `USE_SSL = false` for local development, since the database connection requires SSL by default.

To run locally: 
- `source venv/bin/activate`
- `brew services start postgresql`
- `python -m app.main`

To interact with the database:
- `psql -d tree`
- `\dt` to list tables
- `\q` to quit

When new libraries are installed:
- `pip freeze > requirements.txt`

Deploying:
- `git push`
- `git push heroku main`

Remaining TODO:
- Might want to pause the game when they're not playing