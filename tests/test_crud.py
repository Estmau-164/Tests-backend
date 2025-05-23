from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase
import pytest
import psycopg2

@pytest.fixture
def empleado_datos():
    empleado = EmpleadoBase(
        nombre= "Sergio",
        apellido="Avila",
        tipo_identificacion="DNI",
        numero_identificacion="46474422",
        fecha_nacimiento="2004-02-04",
        correo_electronico="sergioav@gmail.com",
        telefono="11 4035-6286",
        calle="Av. Avellaneda",
        numero_calle= 3512,
        localidad="Virreyes",
        partido="San Fernando",
        provincia="Buenos Aires",
        genero="Masculino",
        pais_nacimiento="Argentina",
        estado_civil="Soltero/a"
    )
    return empleado

def test_crearEmpleadoExitoso(mock_db,empleado_datos):
    cursor = mock_db["cursor"]
    conn = mock_db["conn"]
    cursor.fetchone.return_value = [1, "46474422", "Sergio", "Avila"]

    resultado = AdminCRUD.crear_empleado(empleado_datos)

    assert resultado["numero_identificacion"] == "46474422"
    cursor.execute.assert_called_once()
    conn.commit.assert_called_once()

def test_crearEmpleadoExistente(mock_db,empleado_datos):
    cursor = mock_db["cursor"]
    cursor.fetchone.return_value = [1, "46474422", "Sergio", "Avila"]

    AdminCRUD.crear_empleado(empleado_datos)

    with pytest.raises(ValueError):
        cursor.execute.side_effect = psycopg2.IntegrityError(any)
        AdminCRUD.crear_empleado(empleado_datos)

def test_crearEmpleadoNombreVacio(mock_db, empleado_datos):
    cursor = mock_db["cursor"]
    empleado_datos.nombre = ""
    cursor.execute.side_effect = psycopg2.IntegrityError(any)
    with pytest.raises(Exception):
        AdminCRUD.crear_empleado(empleado_datos)

def test_crearEmpleadoApellidoVacio(mock_db, empleado_datos):
    empleado_datos.apellido = ""
    with pytest.raises(Exception):
        AdminCRUD.crear_empleado(empleado_datos)