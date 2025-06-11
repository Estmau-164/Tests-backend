import pytest
from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase

@pytest.mark.usefixtures("setup_schema")
class TestCreacionUsuario:

    def test_crear_usuario_valido(self):
        raise Exception("Sin terminar")