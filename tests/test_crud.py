from crud.crudAdmintrador import AdminCRUD
from api.schemas import EmpleadoBase
import pytest

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


@pytest.mark.usefixtures("test_db")
class TestCRUD:

    def test_crearEmpleadoExitoso(self):
        resultado = AdminCRUD.crear_empleado(empleado)

        assert resultado["numero_identificacion"] == "46474422"

    def test_crearEmpleadoExistente(self):
        AdminCRUD.crear_empleado(empleado)
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)

    def test_crearEmpleadoSinNombre(self):
        empleado.nombre = ""
        with pytest.raises(ValueError):
            AdminCRUD.crear_empleado(empleado)
