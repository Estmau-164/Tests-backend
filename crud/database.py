import psycopg2
from psycopg2 import pool  # Opcional para connection pooling
import os
from datetime import datetime, timedelta, date, time
from contextlib import contextmanager


# Cargar variables de entorno desde .env


class Database:
    # Configuración para Supabase (actualizada)
    _config = {
        "dbname": "database_labo_test",
        "user": "database_tester_admin",
        "password": "tEstLabO!239",
        "host": "localhost",
        "port": "5432",
        "sslmode": "disable",
        "connect_timeout": 5,
    }

    def __init__(self):
        self.connection_pool = None
        self._initialize_pool()

    def _initialize_pool(self, retries=3, delay=2):
        """Intenta crear el pool de conexiones con reintentos"""
        for attempt in range(retries):
            try:
                self.connection_pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=10,
                    **self._config
                )
                print("✅ Pool de conexiones creado exitosamente")
                return
            except psycopg2.OperationalError as e:
                print(f"⚠️ Intento {attempt + 1} fallido: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(delay)
        raise RuntimeError("No se pudo establecer el pool de conexiones después de varios intentos")

    def get_connection(self):
        """Obtiene una conexión del pool con manejo de errores"""
        try:
            return self.connection_pool.getconn()
        except:
            # Intenta recrear el pool si hay problemas
            self._initialize_pool()
            return self.connection_pool.getconn()

    def return_connection(self, connection):
        """Devuelve una conexión al pool"""
        try:
            self.connection_pool.putconn(connection)
        except:
            # Si hay error al devolver, cierra la conexión
            connection.close()

    def health_check(self):
        """Verifica el estado de la base de datos"""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                return result[0] == 1
        except Exception as e:
            print(f"❌ Error en health check: {str(e)}")
            return False
        finally:
            if conn:
                self.return_connection(conn)

    @contextmanager
    def get_db():
        db = Database(settings.DB_URL)  # Ejemplo con configuración
        try:
            yield db
        finally:
            db.close()


# Instancia global (para uso en otros módulos)
db = Database()