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

To interact with the database locally:
- `psql -d tree`
- `\d` to list tables and views
- `\q` to quit

To interact with the database on Heroku:
- `heroku pg:psql`

When new libraries are installed:
- `pip freeze > requirements.txt`
- Make sure `gunicorn==20.1.0` is included since the above command removes this line

Deploying:
- `git push`
- `git push heroku main`

To view logs:
- `heroku logs --tail`

Remaining TODO:
- Fix timer
- Might want to pause the game when they're not playing
- Sometimes you should scroll to the choice, sometimes to the age
- What's this ERROR:root:Error initializing database: duplicate key value violates unique constraint "pg_type_typname_nsp_index"
- Not seeing my debug logs in Heroku