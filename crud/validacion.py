import re


def nombre_valido(nombre):
    patron = r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$"  # Permite letras, con acento y espacios
    return bool(re.match(patron, nombre))


def apellido_valido(apellido):
    patron = r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$"  # Permite letras, con acento y espacios
    return bool(re.match(patron, apellido))


def correo_electronico_valido(correo_electronico):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"  # Solo el formato de mail
    return bool(re.match(patron, correo_electronico))


def telefono_valido(telefono):
    patron = r"^\+?[\d\s\-()]$"  # Puede iniciar con + y se permiten numeros, espacios, guiones y parentesis
    return bool(re.match(patron, telefono))


def calle_valida(calle):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\.,'\-]+$"  # Se permiten letras, con acento, numeros, espacios y ciertos caracteres especiales
    return bool(re.match(patron, calle))


def numero_calle_valido(numero_calle):
    patron = r"^\d{1,5}$"  # Se permiten solo numeros
    return bool(re.match(patron, numero_calle))


def localidad_valida(localidad):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\.,'\-]+$"  # Se permiten letras, con acento, numeros, espacios y ciertos caracteres especiales
    return bool(re.match(patron, localidad))


def partido_valido(partido):
    patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\.]+$"
    return bool(re.match(patron, partido))


def provincia_valida(provincia):
    provincias_validas = [
        "Buenos Aires",
        "Catamarca",
        "Chaco",
        "Chubut",
        "Córdoba",
        "Corrientes",
        "Entre Ríos",
        "Formosa",
        "Jujuy",
        "La Pampa",
        "La Rioja",
        "Mendoza",
        "Misiones",
        "Neuquén",
        "Río Negro",
        "Salta",
        "San Juan",
        "San Luis",
        "Santa Cruz",
        "Santa Fe",
        "Santiago del Estero",
        "Tierra del Fuego",
        "Tucumán",
        "Ciudad Autónoma de Buenos Aires",
    ]
    if provincia not in provincias_validas:
        return False
    return True


def genero_valido(genero):
    generos_validos = [
        "Masculino",
        "Femenino",
        "No binario",
        "Prefiere no especificar",
        "Otro",
    ]
    if genero not in generos_validos:
        return False
    return True


def pais_nacimiento_valido(pais_nacimiento):
    nacionalidades_validas = [
        "Argentina",
        "Brasil",
        "Chile",
        "Uruguay",
        "Paraguay",
        "Bolivia",
        "Perú",
        "Ecuador",
        "Colombia",
        "Venezuela",
        "México",
    ]
    if pais_nacimiento not in nacionalidades_validas:
        return False
    return True


def tipo_identificacion_valido(tipo_identificacion):
    tipos_identificacion_validos = ["DNI", "Pasaporte", "Cédula"]
    if tipo_identificacion not in tipos_identificacion_validos:
        return False
    return True


def numero_identificacion_valido(tipo_identificacion, numero_identificacion):
    if(tipo_identificacion == "DNI" or tipo_identificacion == "Cédula"):
        return (len(numero_identificacion) >= 7 and numero_identificacion.isdigit())
    elif(tipo_identificacion == "Pasaporte"):
        return (len(numero_identificacion) >= 6 and numero_identificacion.isalnum())
    return False