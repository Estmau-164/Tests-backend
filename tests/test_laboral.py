import pytest
from crud.crudAdmintrador import AdminCRUD
from crud.database import db

def obtener_id_departamento(nombre_departamento: str):
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id_departamento
                FROM departamento
                WHERE nombre = %s
            """,
                (nombre_departamento,),
            )
            resultado = cur.fetchone()
        if resultado is None:
            raise ValueError(f"Departamento con nombre {nombre_departamento} no encontrado")
        
        return resultado
    finally:
        db.return_connection(conn)

@pytest.mark.usefixtures("setup_schema")
class TestDepartamento:

    def test_agregar_departamento_exitoso(self):
        nombre_departamento = "Marketing"
        desc_departamento = "Diseña e implementa estrategias de promoción."
        AdminCRUD.agregar_departamento(nombre_departamento, desc_departamento)

    def test_agregar_departamento_descripcion_vacia(self):
        nombre_departamento = "Marketing"
        desc_departamento = ""
        AdminCRUD.agregar_departamento(nombre_departamento, desc_departamento)

    def test_agregar_departamento_nombre_vacio(self):
        nombre_departamento = ""
        desc_departamento = "Diseña e implementa estrategias de promoción."
        with pytest.raises(Exception):
            AdminCRUD.agregar_departamento(nombre_departamento, desc_departamento)

    def test_agregar_departamento_existente(self):
        nombre_departamento = "Marketing"
        desc_departamento = "Diseña e implementa estrategias de promoción."
        AdminCRUD.agregar_departamento(nombre_departamento, desc_departamento)
        with pytest.raises(Exception):
            AdminCRUD.agregar_departamento(nombre_departamento, desc_departamento)

    def test_listar_departamentos_exitoso(self):
        departamentos = [
            ("Marketing", "Diseña e implementa estrategias de promoción."),
            ("Logística", "Administra almacenamiento y distribución."),
            (
                "Tecnología de la Información (IT)",
                "Gestiona sistemas, redes y soporte técnico.",
            ),
        ]
        for nombre, descripcion in departamentos:
            AdminCRUD.agregar_departamento(nombre, descripcion)

        resultado = AdminCRUD.listar_departamentos()
        nombres = [departamento["nombre"] for departamento in resultado]

        assert len(resultado) == 3
        assert "Marketing" in nombres
        assert "Logística" in nombres
        assert "Tecnología de la Información (IT)" in nombres

    def test_listar_departamentos_sin_departamentos(self):
        resultado = AdminCRUD.listar_departamentos()
        assert len(resultado) == 0

    def test_eliminar_departamento_exitoso(self):
        nombre_departamento = "Marketing"
        desc_departamento = "Diseña e implementa estrategias de promoción."
        AdminCRUD.agregar_departamento(nombre_departamento, desc_departamento)
        
        id_departamento = obtener_id_departamento(nombre_departamento)
        AdminCRUD.eliminar_departamento(id_departamento)

    def test_eliminar_departamento_inexistente(self):
        id_departamento = 1
        with pytest.raises(Exception):
            AdminCRUD.eliminar_departamento(id_departamento)

@pytest.mark.usefixtures("setup_schema")
class TestPuesto:

    def test_agregar_puesto_exitoso(self):
        nombre_puesto = "Analista de Datos"
        AdminCRUD.agregar_puesto(nombre_puesto)

    def test_agregar_puesto_nombre_vacio(self):
        nombre_puesto = ""
        with pytest.raises(Exception):
            AdminCRUD.agregar_puesto(nombre_puesto)

    def test_agregar_puesto_existente(self):
        nombre_puesto = "Analista de Datos"
        AdminCRUD.agregar_puesto(nombre_puesto)
        with pytest.raises(Exception):
            AdminCRUD.agregar_puesto(nombre_puesto)

    def test_listar_puestos_exitoso(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_listar_puestos_sin_puestos(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_eliminar_puesto_exitoso(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_eliminar_puesto_inexistente(self):
        raise NotImplementedError("Test sin terminar")
    
@pytest.mark.usefixtures("setup_schema")
class TestCategoria:

    def test_agregar_categoria_exitoso(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_agregar_categoria_existente(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_agregar_categoria_vacia(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_listar_categorias_exitoso(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_listar_categorias_sin_categorias(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_eliminar_categoria_exitoso(self):
        raise NotImplementedError("Test sin terminar")
    
    def test_eliminar_categoria_inexistente(self):
        raise NotImplementedError("Test sin terminar")