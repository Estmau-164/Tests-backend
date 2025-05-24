import pytest
import psycopg2
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_db():
    with patch("crud.crudAdmintrador.db.conn") as mock_conn:  
        #Simulo cursor
        mock_cursor = MagicMock()
        #Simulo conexion
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        yield {
                "cursor": mock_cursor,
                "conn": mock_conn
        }

@pytest.fixture
def db_connection(postgresql):
    conn = psycopg2.connect(
        dbname=postgresql.info.dbname,
        user=postgresql.info.user,
        password=postgresql.info.password,
        host=postgresql.info.host,
        port=postgresql.info.port
    )

    with conn.cursor() as cur:
        with open("sql/database_test.sql", "r", encoding="utf-8") as f:
            cur.execute(f.read())
    conn.commit()

    yield conn

    conn.rollback()
    conn.close()

