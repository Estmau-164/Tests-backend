import pytest
from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase
from crud.crudUsuario import Usuario
from crud.database import db
import psycopg2


@pytest.fixture
def crear_empleado():
    empleado = EmpleadoBase(
        nombre="Gustavo",
        apellido="Garcia",
        tipo_identificacion="DNI",
        numero_identificacion="46987984",
        fecha_nacimiento="2004-02-04",
        correo_electronico="gusta41@gmail.com",
        telefono="11 4035-6286",
        calle="Quintana",
        numero_calle="2523",
        localidad="Virreyes",
        partido="San Fernando",
        provincia="Buenos Aires",
        genero="Masculino",
        pais_nacimiento="Argentina",
        estado_civil="Casado/a",
    )
    ret = AdminCRUD.crear_empleado(empleado)
    return ret


def obtener_contrasena_usuario(id_usuario: int):
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT contrasena
                FROM usuario
                WHERE id_usuario = %s
            """,
                (id_usuario,),
            )
            resultado = cur.fetchone()

        if resultado is None:
            raise ValueError(f"Usuario con ID {id_usuario} no encontrado")

        password_hash = resultado[0]

        return password_hash
    finally:
        db.return_connection(conn)


@pytest.mark.usefixtures("setup_schema", "cargar_roles")
class TestCrearUsuario:

    def test_crear_usuario_exitoso(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        Usuario.crear_usuario(id_empleado, 1, "Flow_123", "contrA45!", None)

    def test_crear_usuario_nombre_un_caracter(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        Usuario.crear_usuario(id_empleado, 1, "a", "contrA45!", None)

    def test_crear_usuario_nombre_con_espacios(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        with pytest.raises(Exception):
            Usuario.crear_usuario(id_empleado, 1, "Gus Gar", "contrA45!", None)

    def test_crear_usuario_nombre_vacio(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        with pytest.raises(Exception):
            Usuario.crear_usuario(id_empleado, 1, "", "contrA45!", None)

    def test_crear_usuario_contrasena_ocho_caracteres(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        Usuario.crear_usuario(id_empleado, 1, "Flow_123", "contrA4!", None)

    def test_crear_usuario_contrasena_corta(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        with pytest.raises(Exception):
            Usuario.crear_usuario(
                id_empleado, 1, "Flow_123", "contr4!", None
            )  # Contrasena de 7 caracteres

    def test_crear_usuario_contrasena_sin_caracteres_especiales(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        Usuario.crear_usuario(id_empleado, 1, "Flow_123", "contrA45", None)

    def test_crear_usuario_contrasena_sin_letras(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        with pytest.raises(Exception):
            Usuario.crear_usuario(id_empleado, 1, "Flow_123", "5492!235", None)

    def test_crear_usuario_contraseña_sin_numeros(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        with pytest.raises(Exception):
            Usuario.crear_usuario(id_empleado, 1, "Flow_123", "passsegura!", None)

    def test_crear_usuario_contraseña_vacia(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        with pytest.raises(Exception):
            Usuario.crear_usuario(id_empleado, 1, "Flow_123", "", None)

    def test_crear_usuario_dos_veces(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        Usuario.crear_usuario(id_empleado, 1, "Flow_123", "contrA45!", None)
        with pytest.raises(Exception):
            Usuario.crear_usuario(id_empleado, 1, "GusGar123", "contrA45!", None)


@pytest.mark.usefixtures("setup_schema", "cargar_roles")
class TestVerificarContrasena:

    def test_verificar_contrasena_exitoso(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        id_usuario = Usuario.crear_usuario(
            id_empleado, 1, "Flow_123", "contrA45!", None
        )
        contrasena_hash = obtener_contrasena_usuario(id_usuario)
        assert Usuario.verificar_password("contrA45!", contrasena_hash) == True

    def test_verificar_contrasena_fallido(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        id_usuario = Usuario.crear_usuario(
            id_empleado, 1, "Flow_123", "contrA45!", None
        )
        contrasena_hash = obtener_contrasena_usuario(id_usuario)
        assert Usuario.verificar_password("contrA45", contrasena_hash) == False


@pytest.mark.usefixtures("setup_schema", "cargar_roles")
class TestObtenerUsuario:

    def test_obtener_usuario_exitoso(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        Usuario.crear_usuario(id_empleado, 1, "Flow_123", "contrA45!", None)
        usuario_obtenido = Usuario.obtener_usuario_por_username("Flow_123")
        assert id_empleado == usuario_obtenido.id_empleado

    def test_obtener_usuario_inexistente(self, crear_empleado):
        id_empleado = crear_empleado["id_empleado"]
        Usuario.crear_usuario(id_empleado, 1, "Flow_123", "contrA45!", None)
        no_existe_usuario = (
            True if Usuario.obtener_usuario_por_username("Gar_123") == None else False
        )
        assert no_existe_usuario == True
