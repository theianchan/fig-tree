# fig-tree

To install on a new machine:
- `brew install python@3.12`
- `python3.12 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `brew tap heroku/brew && brew install heroku`
- `heroku login`
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
- `heroku pg:psql --app fig-tree`
- `\d`
- `\d table_name`

When new libraries are installed:
- `pip freeze > requirements.txt`
- Make sure `gunicorn==20.1.0` is included since the above command removes this line

Currently manually tracking requirements to get around the tokenizers thing:
```
anthropic==0.42.0
Flask==3.0.3
Flask-Caching==2.1.0
Flask-SQLAlchemy==3.1.1
gunicorn==20.1.0
psycopg2-binary==2.9.9
python-dotenv==1.0.1
SQLAlchemy==2.0.35
```

Deploying:
- `git push`
- `git push heroku main`

To view logs:
- `heroku logs --tail --app fig-tree`

Remaining TODO:
- Fix timer
- Might want to pause the game when they're not playing
- Sometimes you should scroll to the choice, sometimes to the age
- What's this ERROR:root:Error initializing database: duplicate key value violates unique constraint "pg_type_typname_nsp_index"
- Not seeing my debug logs in Heroku