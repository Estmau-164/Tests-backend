import pytest
from crud.database import Database
from crud import crudAdmintrador
from testcontainers.postgres import PostgresContainer
import os


@pytest.fixture
def test_db():
    db_config = {
        "dbname": "database_labo_test",
        "user": "database_tester_admin",
        "password": "tEstLabO!239",
        "host": "localhost",
        "port": "5432",
        "sslmode": "require",
        "connect_timeout": 5,
    }

    # Instancia con la configuración temporal
    db_instance = Database()
    db_instance._config = db_config

    crudAdmintrador.db = db_instance

    # Cargar archivo SQL con tablas y triggers
    schema_path = os.path.join(os.path.dirname(__file__), "sql", "test_schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn = db_instance.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
    finally:
        db_instance.return_connection(conn)

    yield db_instance