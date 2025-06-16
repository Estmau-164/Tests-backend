import pytest
from crud import validacion_entrada


def test_validar_nombre_valido():
    validacion_entrada.validar_nombre("Mauro")


@pytest.mark.parametrize("nombre", ["M4uro", "Juan!", "Esteban123#"])
def test_validar_nombre_invalido(nombre):
    with pytest.raises(Exception):
        validacion_entrada.validar_nombre(nombre)


def test_validar_apellido_valido():
    validacion_entrada.validar_apellido("Palavecino")


@pytest.mark.parametrize("apellido", ["P4lav3cino", "A#vi$", "Ramir3z!"])
def test_validar_apellido_invalido(apellido):
    with pytest.raises(Exception):
        validacion_entrada.validar_apellido(apellido)


@pytest.mark.parametrize("tipo_identificacion", ["DNI", "Pasaporte", "Cédula"])
def test_validar_tipo_identificacion_valido(tipo_identificacion):
    validacion_entrada.validar_tipo_identificacion(tipo_identificacion)


@pytest.mark.parametrize("tipo_identificacion", ["Sube", "Licencia de conducir"])
def test_validar_tipo_identificacion_invalida(tipo_identificacion):
    with pytest.raises(Exception):
        validacion_entrada.validar_tipo_identificacion(tipo_identificacion)


def test_validar_numero_identificacion_valida():
    validacion_entrada.validar_numero_identificacion("DNI", "49801921")
    validacion_entrada.validar_numero_identificacion("Pasaporte", "AB164132")
    validacion_entrada.validar_numero_identificacion("Cédula", "49801921")


def test_validar_correo_electronico_valido():
    validacion_entrada.validar_correo_electronico("usuario@gmail.com")


@pytest.mark.parametrize(
    "correo_electronico", ["usuario@gmail", "usuario@.com", "@gmail.com"]
)
def test_validar_correo_electronico_invalido(correo_electronico):
    with pytest.raises(Exception):
        validacion_entrada.validar_correo_electronico(correo_electronico)


@pytest.mark.parametrize(
    "telefono", ["11 4455-5454", "+54 11 4455-5454", "1144555454", "(011) 4455-5454"]
)
def test_validar_telefono_valido(telefono):
    validacion_entrada.validar_telefono(telefono)


@pytest.mark.parametrize("telefono", ["12d3-434s", "341#!-=sdq"])
def test_validar_telefono_invalido(telefono):
    with pytest.raises(Exception):
        validacion_entrada.validar_telefono(telefono)


@pytest.mark.parametrize("calle", ["Av. San Martín", "O'Higgins", "Quintana"])
def test_validar_calle_valida(calle):
    validacion_entrada.validar_calle(calle)


@pytest.mark.parametrize("calle", ["Av. San Martín, 2465", "G#ndolf?"])
def test_validar_calle_invalida(calle):
    with pytest.raises(Exception):
        validacion_entrada.validar_calle(calle)


def test_validar_numero_calle_valido():
    validacion_entrada.validar_numero_calle("5")
    validacion_entrada.validar_numero_calle("12")
    validacion_entrada.validar_numero_calle("786")
    validacion_entrada.validar_numero_calle("1321")
    validacion_entrada.validar_numero_calle("10568")


@pytest.mark.parametrize("numero_calle", ["456a", "45!="])
def test_validar_numero_calle_invalido(numero_calle):
    with pytest.raises(Exception):
        validacion_entrada.validar_numero_calle(numero_calle)


@pytest.mark.parametrize("localidad", ["Virreyes", "José C. Paz"])
def test_validar_localidad_valida(localidad):
    validacion_entrada.validar_localidad(localidad)


@pytest.mark.parametrize(
    "localidad", ["La Plata, Buenos Aires", "Córdoba!", "José C. Paz!"]
)
def test_validar_localidad_invalida(localidad):
    with pytest.raises(Exception):
        validacion_entrada.validar_localidad(localidad)


def test_validar_partido_valido():
    validacion_entrada.validar_partido("Malvinas Argentinas")


def test_validar_partido_invalido():
    with pytest.raises(Exception):
        validacion_entrada.validar_partido("M4lvinas Arg*n!nas")


def test_validar_provincia_valida():
    validacion_entrada.validar_provincia("Buenos Aires")
    validacion_entrada.validar_provincia("Jujuy")


def test_validar_provincia_invalida():
    with pytest.raises(Exception):
        validacion_entrada.validar_provincia("Antartida Argentina")


def test_validar_pais_nacimiento_valido():
    validacion_entrada.validar_pais_nacimiento("Argentina")
    validacion_entrada.validar_pais_nacimiento("Uruguay")
    validacion_entrada.validar_pais_nacimiento("Chile")


def test_validar_pais_nacimiento_invalido():
    with pytest.raises(Exception):
        validacion_entrada.validar_pais_nacimiento("Wakanda")


def test_validar_genero_valido():
    validacion_entrada.validar_genero("Femenino")
    validacion_entrada.validar_genero("Masculino")
    validacion_entrada.validar_genero("No binario")


def test_validar_genero_invalido():
    with pytest.raises(Exception):
        validacion_entrada.validar_genero("Plantae")


def test_validar_estado_civil_valido():
    validacion_entrada.validar_estado_civil("Soltero/a")
    validacion_entrada.validar_estado_civil("Casado/a")


def test_validar_estado_civil_invalido():
    with pytest.raises(Exception):
        validacion_entrada.validar_estado_civil("En pareja")
