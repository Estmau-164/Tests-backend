import pytest
from api.schemas import EmpleadoBase2
from crud.crudAdmintrador import AdminCRUD
from crud.crudEmpleado import Empleado
from crud.crudUsuario import Usuario
import unicodedata


@pytest.fixture
def datos_empleados():
    empleado0 = EmpleadoBase2(
        nombre="José",
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
    empleado1 = EmpleadoBase2(
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


@pytest.mark.usefixtures("setup_schema")
class TestCreacionEmpleado:

    def test_crear_empleado_exitoso(self, datos_empleados):
        empleadoDni = datos_empleados[0]
        empleadoPasaporte = datos_empleados[1]
        assert (
            AdminCRUD.crear_empleado3(empleadoDni)["numero_identificacion"] == "46474422"
        )
        assert (
            AdminCRUD.crear_empleado3(empleadoPasaporte)["numero_identificacion"]
            == "AB465412"
        )

    def test_crear_empleado_existente(self, datos_empleados):
        empleado = datos_empleados[0]
        AdminCRUD.crear_empleado3(empleado)
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_nombre_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.nombre = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_apellido_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.apellido = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_tipo_identificacion_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.tipo_identificacion = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_nro_identificacion_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.numero_identificacion = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_fecha_nacimiento_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.fecha_nacimiento = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_correo_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.correo_electronico = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_telefono_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.telefono = ""
        # El sistema me deberia dejar registrar un empleado sin telefono
        assert AdminCRUD.crear_empleado3(empleado)["numero_identificacion"] == "46474422"

    @pytest.mark.parametrize("telefono_invalido", ["12d3-434s", "341#!-=sdq"])
    def test_crear_empleado_telefono_invalido(self, datos_empleados, telefono_invalido):
        empleado = datos_empleados[0]
        empleado.telefono = telefono_invalido
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)["numero_identificacion"] == "46474422"

    def test_crear_empleado_calle_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.calle = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_numero_calle_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.numero_calle = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_localidad_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.localidad = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_partido_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.partido = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_provincia_vacia(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.provincia = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_pais_nacimiento_vacio(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.pais_nacimiento = ""
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    @pytest.mark.parametrize("nombre_invalido", ["S3rgi0", "Serg!*"])
    def test_crear_empleado_nombre_invalido(self, datos_empleados, nombre_invalido):
        empleado = datos_empleados[0]
        empleado.nombre = nombre_invalido
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    @pytest.mark.parametrize("apellido_invalido", ["4v1la", "Avi!l*"])
    def test_crear_empleado_apellido_invalido(self, datos_empleados, apellido_invalido):
        empleado = datos_empleados[0]
        empleado.apellido = apellido_invalido
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    @pytest.mark.parametrize(
        "tipo_identificacion_invalido", ["Licencia de conducir", "Sube"]
    )
    def test_crear_empleado_tipo_identificacion_invalida(
        self, datos_empleados, tipo_identificacion_invalido
    ):
        empleado = datos_empleados[0]
        empleado.tipo_identificacion = tipo_identificacion_invalido
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    @pytest.mark.parametrize("numero_dni_invalido", ["44thf68a", "44621*!?"])
    def test_crear_empleado_numero_identificacion_dni_invalido(
        self, datos_empleados, numero_dni_invalido
    ):
        empleado = datos_empleados[0]
        empleado.numero_identificacion = numero_dni_invalido
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_numero_identificacion_pasaporte_invalido(
        self, datos_empleados
    ):
        empleado = datos_empleados[1]
        empleado.numero_identificacion = "AF*41!84?"
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    @pytest.mark.parametrize(
        "fecha_nacimiento_invalida",
        ["2004-00-04", "2004-02-00", "2004-13-00", "2004-02-30"],
    )
    def test_crear_empleado_fecha_nacimiento_mes_dia_invalido(
        self, datos_empleados, fecha_nacimiento_invalida
    ):
        empleado = datos_empleados[0]
        empleado.fecha_nacimiento = fecha_nacimiento_invalida
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    def test_crear_empleado_fecha_nacimiento_formato_invalido(self, datos_empleados):
        empleado = datos_empleados[0]
        empleado.fecha_nacimiento = "4 de febrero 2004"
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    @pytest.mark.parametrize(
        "numero_calle_invalido", ["mildoscientos cuarenta y dos", "14*!"]
    )
    def test_crear_empleado_numero_calle_invalido(
        self, datos_empleados, numero_calle_invalido
    ):
        empleado = datos_empleados[0]
        empleado.numero_calle = numero_calle_invalido
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)

    @pytest.mark.parametrize(
        "correo_invalido",
        ["sergioav@gmail", "sergioavgmail.com", "@gmail.com", "sergioav@.com"],
    )
    def test_crear_empleado_correo_invalido(self, datos_empleados, correo_invalido):
        empleado = datos_empleados[0]
        empleado.correo_electronico = correo_invalido
        with pytest.raises(Exception):
            AdminCRUD.crear_empleado3(empleado)


@pytest.mark.usefixtures("setup_schema")
class TestEliminarEmpleado:

    def test_eliminar_empleado_existente(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        assert Empleado.borrar_por_id(nuevo_empleado["id_empleado"]) == True

    def test_eliminar_empleado_inexistente(self):
        assert Empleado.borrar_por_id(1) == False


@pytest.mark.usefixtures("setup_schema")
class TestObtenerEmpleado:
    def test_obtener_empleado_existente_por_id(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        empleado_obtenido = Empleado.obtener_por_id(nuevo_empleado["id_empleado"])
        assert (
            empleado_obtenido.numero_identificacion
            == nuevo_empleado["numero_identificacion"]
        )

    def test_obtener_empleado_inexistente_por_id(self):
        assert Empleado.obtener_por_id(1) == None


@pytest.mark.usefixtures("setup_schema","cargar_roles")
class TestActualizarDatosEmpleado:
    def test_actualizar_datos_empleado_existente(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        empleado_actualizado = AdminCRUD.actualizar_datos_personales2(
            1,
            nuevo_empleado["id_empleado"],
            "11 5498-3219",
            "nuevocorreo@gmail.com",
            "Brasil",
            "6543",
            "Polvorines",
            "Malvinas Argentinas",
            "Buenos Aires",
        )
        assert empleado_actualizado.telefono == "11 5498-3219"
        assert empleado_actualizado.correo_electronico == "nuevocorreo@gmail.com"
        assert empleado_actualizado.calle == "Brasil"
        assert empleado_actualizado.numero_calle == "6543"
        assert empleado_actualizado.localidad == "Polvorines"
        assert empleado_actualizado.partido == "Malvinas Argentinas"
        assert empleado_actualizado.provincia == "Buenos Aires"

    def test_actualizar_datos_empleado_inexistente(self):
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                1,
                "11 5498-3219",
                "nuevocorreo@gmail.com",
                "Brasil",
                "6543",
                "Polvorines",
                "Malvinas Argentinas",
                "Buenos Aires",
            )

    def test_actualizar_ningun_dato_empleado(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )

    @pytest.mark.parametrize("telefono_invalido", ["12d3-434s", "341#!-=sdq"])
    def test_actualizar_datos_empleado_telefono_invalido(
        self, datos_empleados, telefono_invalido
    ):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                telefono_invalido,
                "nuevocorreo@gmail.com",
                "Brasil",
                "6543",
                "Polvorines",
                "Malvinas Argentinas",
                "Buenos Aires",
            )

    @pytest.mark.parametrize(
        "correo_invalido", ["usuario@gmail", "usuario@.com", "@gmail.com"]
    )
    def test_actualizar_datos_empleado_correo_invalido(
        self, datos_empleados, correo_invalido
    ):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                "11 5498-3219",
                correo_invalido,
                "Brasil",
                "6543",
                "Polvorines",
                "Malvinas Argentinas",
                "Buenos Aires",
            )

    def test_actualizar_datos_empleado_calle_invalida(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                "11 5498-3219",
                "nuevocorreo@gmail.com",
                "G#ndolf?",
                "6543",
                "Polvorines",
                "Malvinas Argentinas",
                "Buenos Aires",
            )

    def test_actualizar_datos_empleado_numero_calle_invalido(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                "11 5498-3219",
                "nuevocorreo@gmail.com",
                "Brasil",
                "654a",
                "Polvorines",
                "Malvinas Argentinas",
                "Buenos Aires",
            )

    @pytest.mark.parametrize(
        "localidad_invalida", ["La Plata, Buenos Aires", "Córdoba!"]
    )
    def test_actualizar_datos_empleado_localidad_invalida(
        self, datos_empleados, localidad_invalida
    ):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                "11 5498-3219",
                "nuevocorreo@gmail.com",
                "Brasil",
                "6543",
                localidad_invalida,
                "Malvinas Argentinas",
                "Buenos Aires",
            )

    def test_actualizar_datos_empleado_partido_invalido(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                "11 5498-3219",
                "nuevocorreo@gmail.com",
                "Brasil",
                "6543",
                "Polvorines",
                "M4lvinas Arg*n!nas",
                "Buenos Aires",
            )

    def test_actualizar_datos_empleado_provincia_invalida(self, datos_empleados):
        nuevo_empleado = AdminCRUD.crear_empleado3(datos_empleados[0])
        Usuario.crear_usuario(nuevo_empleado["id_empleado"],1,"NuevoUsuario","contra123",None)
        with pytest.raises(Exception):
            AdminCRUD.actualizar_datos_personales2(
                1,
                nuevo_empleado["id_empleado"],
                "11 5498-3219",
                "nuevocorreo@gmail.com",
                "Brasil",
                "6543",
                "Polvorines",
                "Malvinas Argentinas",
                "Antartida Argentina",
            )
