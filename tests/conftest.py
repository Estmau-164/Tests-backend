import pytest
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