# Authentication server python microservice

## Steps to get started
- create a virtual environment using python3
- see: https://virtualenvwrapper.readthedocs.io/en/latest/

### dependencies
- `brew install postgresql`
- `brew install openssl`
- `export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/`

### to install
- `pip install -e .`

### to run
- `pserve development.ini [--reload]`

### Migrations
#### to init alembic
- `alembic init alembic`
#### to create new migrations
- `alembic revision -m "migration short description"`
- Update the functions upgrade and downgrade created in the file named `[id]_migration_short_description.py` in `PATH/alembic/versions`
#### to run migrations
- `alembic upgrade [head | migration id]`
#### to revert migrations
- `alembic upgrade [base | migration id]`


### notes
- Run tests via `pytest`
- Configured with `sqlalchemy`
- Database migrations with `alembic`
