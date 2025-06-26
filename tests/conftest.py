import pytest
from crud.database import db
from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase2
import os


# Limpia la base de datos antes de cada test
@pytest.fixture
def setup_schema():
    # Cargar archivo SQL con tablas y triggers
    schema_path = os.path.join(os.path.dirname(__file__), "sql", "test_schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        db.return_connection(conn)


@pytest.fixture
def cargar_roles():
    roles_path = os.path.join(os.path.dirname(__file__), "sql", "roles.sql")
    with open(roles_path, "r", encoding="utf-8") as f:
        roles_sql = f.read()
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(roles_sql)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        db.return_connection(conn)