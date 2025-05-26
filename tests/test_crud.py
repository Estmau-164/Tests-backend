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
        pais_nacimiento="Uruguay",
        estado_civil="Casado/a",
    )
    return [empleado0, empleado1]


@pytest.mark.usefixtures("test_db", "setup_schema")
class TestCreacionEmpleado:

    def test_crear_empleado_exitoso(self, datos_empleados):
        empleadoDni = datos_empleados[0]
        empleadoPasaporte = datos_empleados[1]
        assert (
            AdminCRUD.crear_empleado(empleadoDni)["numero_identificacion"] == "46474422"
        )
        assert (
            AdminCRUD.crear_empleado(empleadoPasaporte)["numero_identificacion"]
            == "AB465412"
        )

    def test_crear_empleado_existente(self, datos_empleados):
        empleado = datos_empleados[0]
        AdminCRUD.crear_empleado(empleado)
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_nombre_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.nombre = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_apellido_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.apellido = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_tipo_identificacion_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.tipo_identificacion = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_nro_identificacion_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.numero_identificacion = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_fecha_nacimiento_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.fecha_nacimiento = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_correo_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.correo_electronico = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_telefono_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.telefono = ""
        # El sistema me deberia dejar registrar un empleado sin telefono
        assert AdminCRUD.crear_empleado(empleado)["numero_identificacion"] == "46474422"

    def test_crear_empleado_calle_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.calle = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_numero_calle_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.numero_calle = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_localidad_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.localidad = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_partido_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.partido = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_provincia_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.provincia = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_pais_nacimiento_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.pais_nacimiento = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    @pytest.mark.parametrize("nombre_invalido", ["S3rgi0", "Serg!*"])
    def test_crear_empleado_nombre_invalido(self, datos_empleados, nombre_invalido):
        empleado = datos_empleados[0]
        empleado.nombre = nombre_invalido
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    @pytest.mark.parametrize("apellido_invalido", ["4v1la", "Avi!l*"])
    def test_crear_empleado_apellido_invalido(self, datos_empleados, apellido_invalido):
        empleado = datos_empleados[0]
        empleado.apellido = apellido_invalido
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    @pytest.mark.parametrize(
        "tipo_identificacion_invalido", ["Licencia de conducir", "Sube"]
    )
    def test_crear_empleado_tipo_identificacion_invalida(
        self, datos_empleados, tipo_identificacion_invalido
    ):
        empleado = datos_empleados[0]
        empleado.tipo_identificacion = tipo_identificacion_invalido
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    @pytest.mark.parametrize("numero_dni_invalido", ["44thf68a","44621*!?"])
    def test_crear_empleado_numero_identificacion_dni_invalido(self,datos_empleados,numero_dni_invalido):
        empleado = datos_empleados[0]
        empleado.numero_identificacion = numero_dni_invalido
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crear_empleado_numero_identificacion_pasaporte_invalido(self, datos_empleados):
        empleado = datos_empleados[1]
        empleado.numero_identificacion = "AF*41!84?"
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    @pytest.mark.parametrize("fecha_nacimiento_invalida", ["2004-00-04","2004-02-00","2004-13-00","2004-02-30"])
    def test_crear_empleado_fecha_nacimiento_invalida(self, datos_empleados, fecha_nacimiento_invalida):
        empleado = datos_empleados[0]
        empleado.fecha_nacimiento = fecha_nacimiento_invalida
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)