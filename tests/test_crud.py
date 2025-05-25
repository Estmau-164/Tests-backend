from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase
import pytest
import psycopg2
import crud.crudAdmintrador as crudAdmintrador


@pytest.fixture
def empleado_datos():
    empleado = EmpleadoBase(
        nombre="Sergio",
        apellido="Avila",
        tipo_identificacion="DNI",
        numero_identificacion="46474422",
        fecha_nacimiento="2004-02-04",
        correo_electronico="sergioav@gmail.com",
        telefono="11 4035-6286",
        calle="Av. Avellaneda",
        numero_calle="3512",
        localidad="Virreyes",
        partido="San Fernando",
        provincia="Buenos Aires",
        genero="Masculino",
        pais_nacimiento="Argentina",
        estado_civil="Soltero/a",
    )
    return empleado

@pytest.mark.usefixtures("test_db")
class TestCRUD:
    def test_crearEmpleadoExitoso(self, empleado_datos):
        resultado = AdminCRUD.crear_empleado(empleado_datos)

        assert resultado["numero_identificacion"] == "46474422"

    def test_crearEmpleadoExistente(self, empleado_datos):
        AdminCRUD.crear_empleado(empleado_datos)
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado_datos)