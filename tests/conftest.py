import pytest
from crud.database import db
from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase
import os

# Limpia la base de datos antes de cada test
@pytest.fixture
def setup_schema():
    # Cargar archivo SQL con tablas y triggers
    schema_path = os.path.join(os.path.dirname(__file__), "sql", "test_schema.sql")
    inserts_path = os.path.join(os.path.dirname(__file__), "sql", "inserts.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    with open(inserts_path, "r") as f:
        inserts_sql = f.read()

    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            cur.execute(inserts_sql)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        db.return_connection(conn)