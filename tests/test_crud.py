from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase
import pytest


@pytest.fixture
def datos_empleados():
    empleado0 = EmpleadoBase(
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
    empleado1 = EmpleadoBase(
        nombre="Carlos",
        apellido="Gutierrez",
        tipo_identificacion="Pasaporte",
        numero_identificacion="AB465412",
        fecha_nacimiento="2005-05-15",
        correo_electronico="cargut@gmail.com",
        telefono="11 1987-4984",
        calle="Lavalle",
        numero_calle="3512",
        localidad="Tigre",
        partido="Tigre",
        provincia="Buenos Aires",
        genero="Masculino",
        pais_nacimiento="Perú",
        estado_civil="Casado/a",
    )
    return [empleado0, empleado1]


@pytest.mark.usefixtures("test_db", "setup_schema")
class TestCRUD:

    def test_crearEmpleadoExitoso(self, datos_empleados):
        empleadoDni = datos_empleados[0]
        empleadoPasaporte = datos_empleados[1]
        assert AdminCRUD.crear_empleado(empleadoDni)["numero_identificacion"] == "46474422"
        assert AdminCRUD.crear_empleado(empleadoPasaporte)["numero_identificacion"] == "AB465412"

    def test_crearEmpleadoExistente(self, datos_empleados):
        empleado = datos_empleados[0]
        AdminCRUD.crear_empleado(empleado)
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crearEmpleadoSinNombre(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.nombre = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crearEmpleadoSinApellido(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.apellido = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)
 
    def test_crearEmpleadoSinTipoIdentificacion(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.tipo_identificacion = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)