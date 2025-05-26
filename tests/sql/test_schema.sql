
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


CREATE TABLE empleado (
    id_empleado SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    tipo_identificacion VARCHAR(20) NOT NULL CHECK (tipo_identificacion IN ('DNI', 'Pasaporte', 'Cédula')),
    numero_identificacion VARCHAR(30) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    calle VARCHAR(100) NOT NULL,
    numero_calle VARCHAR(10),
    localidad VARCHAR(50) NOT NULL,
    partido VARCHAR(50) NOT NULL,
    provincia VARCHAR(50) NOT NULL CHECK (
    provincia IN (
        'Buenos Aires', 'Catamarca', 'Chaco', 'Chubut', 'Córdoba', 'Corrientes',
        'Entre Ríos', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza',
        'Misiones', 'Neuquén', 'Río Negro', 'Salta', 'San Juan', 'San Luis',
        'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucumán',
        'Ciudad Autónoma de Buenos Aires'
    )
	),
    genero VARCHAR(30) CHECK (genero IN ('Masculino', 'Femenino', 'No binario', 'Prefiere no especificar', 'Otro')),
    pais_nacimiento VARCHAR(30) NOT NULL CHECK (pais_nacimiento IN ('Argentina', 'Brasil', 'Chile', 'Uruguay', 'Paraguay', 'Bolivia', 'Perú', 'Ecuador', 'Colombia', 'Venezuela', 'México')),
    estado_civil VARCHAR(30) CHECK (estado_civil IN ('Soltero/a', 'Casado/a', 'Divorciado/a', 'Viudo/a'))
);

CREATE TABLE periodo_empleado (
    id_periodo SERIAL PRIMARY KEY,
    id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
    periodo_fecha DATE NOT NULL, 
    presentismo BOOLEAN NOT NULL DEFAULT TRUE,
    porcentaje_asistencia NUMERIC(5,2), 
    faltas_justificadas INTEGER DEFAULT 0,
    faltas_injustificadas INTEGER DEFAULT 0,
    periodo_texto VARCHAR(20), 
    valor_hora NUMERIC(10,2),
    UNIQUE(id_empleado,periodo_fecha)
);

CREATE TABLE rol (
    id_rol SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(50) NOT NULL UNIQUE,
	fecha_creacion DATE NOT NULL,
	online_login BOOLEAN DEFAULT FALSE,
	offline_login BOOLEAN DEFAULT FALSE,
	ver_datos_empleado BOOLEAN DEFAULT FALSE,
    editar_datos_empleado BOOLEAN DEFAULT FALSE,
    ver_registro_asistencia BOOLEAN DEFAULT FALSE,
    editar_registro_asistencia BOOLEAN DEFAULT FALSE,
    ver_recibos_sueldo BOOLEAN DEFAULT FALSE,
    ver_horas_extra BOOLEAN DEFAULT FALSE,
    editar_horas_extra BOOLEAN DEFAULT FALSE,
    ver_nomina BOOLEAN DEFAULT FALSE,
    descargar_nomina BOOLEAN DEFAULT FALSE,
    enviar_notificaciones BOOLEAN DEFAULT FALSE,
    configurar_modelos_ml BOOLEAN DEFAULT FALSE,
    ver_datos_modelos_ml BOOLEAN DEFAULT FALSE,
    aprobar_solicitudes BOOLEAN DEFAULT FALSE,
    descripcion TEXT
);

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY NOT NULL,
    id_empleado INTEGER NOT NULL UNIQUE REFERENCES empleado(id_empleado),
    id_rol INTEGER NOT NULL REFERENCES rol(id_rol),
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    esta_Activo BOOLEAN DEFAULT FALSE,
    fecha_activacion DATE,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
	motivo TEXT
);

CREATE TABLE dato_biometrico_facial(
	id_biometrico SERIAL PRIMARY KEY NOT NULL,
	id_empleado INTEGER NOT NULL UNIQUE REFERENCES empleado(id_empleado),
	vector_biometrico TEXT UNIQUE NOT NULL
);

CREATE TABLE departamento(
	id_departamento SERIAL PRIMARY KEY NOT NULL,
	nombre VARCHAR(50) NOT NULL,
	descripcion VARCHAR(50)
);

CREATE TABLE puesto (
    id_puesto SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE categoria (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE banco (
    id_banco SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE cuenta_bancaria (
    id_cuenta SERIAL PRIMARY KEY,
    id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
    id_banco INTEGER NOT NULL REFERENCES banco(id_banco),
    numero_cuenta VARCHAR(30) NOT NULL,
    tipo_cuenta VARCHAR(30) CHECK (tipo_cuenta IN ('Caja de ahorro', 'Cuenta corriente'))
);

CREATE TABLE nomina (
    id_nomina SERIAL PRIMARY KEY,
    id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
    id_periodo INTEGER NOT NULL REFERENCES periodo_empleado(id_periodo),
    fecha_de_pago DATE NOT NULL,

    salario_base NUMERIC(10,2) NOT NULL,
    bono_presentismo NUMERIC(10,2),
    bono_antiguedad NUMERIC(10,2),
    horas_extra NUMERIC(10,2),

    descuento_jubilacion NUMERIC(10,2),
    descuento_obra_social NUMERIC(10,2),
    descuento_anssal NUMERIC(10,2),
    descuento_ley_19032 NUMERIC(10,2),
    impuesto_ganancias NUMERIC(10,2),
    descuento_sindical NUMERIC(10,2),

    sueldo_bruto NUMERIC(10,2) NOT NULL,
    sueldo_neto NUMERIC(10,2) NOT NULL,

    estado VARCHAR(20) CHECK (estado IN ('Pendiente', 'En proceso', 'Pagada')) DEFAULT 'Pendiente',
    UNIQUE(id_empleado, id_periodo)
);

CREATE TABLE concepto(
    codigo VARCHAR(10) PRIMARY KEY NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    tipo_concepto VARCHAR(20) NOT NULL CHECK (tipo_concepto IN ('Remunerativo','No remunerativo','Deducción','Retención','Percepción',
    'Indemnización','Reintegro','Premio','Multa','Ajuste','Anticipo','Vacaciones')),
    valor_por_defecto NUMERIC(10, 2),
    es_porcentaje BOOLEAN DEFAULT false
);

CREATE TABLE empleado_concepto (
    id_empleado INTEGER REFERENCES empleado(id_empleado),
    codigo_concepto VARCHAR(10) REFERENCES concepto(codigo),
    PRIMARY KEY(id_empleado, codigo_concepto)
);

CREATE TABLE bono_antiguedad (
    años INTEGER PRIMARY KEY,
    porcentaje NUMERIC(5,2) NOT NULL CHECK (porcentaje >= 0)
);

CREATE TABLE salario_base (
    id_salario_base SERIAL PRIMARY KEY,
    id_puesto INTEGER NOT NULL REFERENCES puesto(id_puesto),
    id_departamento INTEGER NOT NULL REFERENCES departamento(id_departamento),
    id_categoria INTEGER NOT NULL REFERENCES categoria(id_categoria),

    valor_por_defecto NUMERIC(10,2) NOT NULL,

    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,

    CHECK (fecha_fin IS NULL OR fecha_fin > fecha_inicio),

    UNIQUE(id_puesto, id_departamento, id_categoria, fecha_inicio)
);


CREATE TABLE registro_jornada (
    id_registro_jornada SERIAL PRIMARY KEY NOT NULL,
    id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
    id_periodo INTEGER NOT NULL REFERENCES periodo_empleado(id_periodo),
    fecha DATE NOT NULL,
    dia VARCHAR(30) NOT NULL CHECK (dia IN ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo')),	
    hora_entrada TIME NOT NULL,
    hora_salida TIME NOT NULL,
    estado_jornada VARCHAR(30)NOT NULL CHECK (estado_jornada IN ('Completa','Completa con horas extra','Incompleta')),
    horas_normales_trabajadas INTEGER NOT NULL,
    observaciones TEXT,
    UNIQUE (id_empleado, id_periodo, fecha)
);

CREATE TABLE registro_hora_extra (
    id_registro_hora_extra SERIAL PRIMARY KEY NOT NULL,
    id_registro_jornada INTEGER NOT NULL REFERENCES registro_jornada(id_registro_jornada),
    cantidad_horas INTEGER NOT NULL CHECK (cantidad_horas > 0),
    tipo_hora_extra VARCHAR(10) NOT NULL CHECK (tipo_hora_extra IN ('50%', '100%')),
    observaciones TEXT
);

CREATE TABLE feriado (
    fecha DATE PRIMARY KEY,
    descripcion TEXT NOT NULL
);


CREATE TABLE documento(
	id_documento SERIAL PRIMARY KEY NOT NULL,
	id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
	tipo VARCHAR(30) NOT NULL CHECK (tipo IN (
  	'DNI', 'CUIL', 'Partida de nacimiento', 'CV', 'Título', 
  	'Domicilio', 'AFIP', 'Foto', 'CBU', 'Certificado médico', 
  	'Licencia de conducir', 'Contrato', 'Otros'
	)),
	fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	archivo_asociado TEXT NOT NULL,
	descripcion TEXT	
);

CREATE TABLE asistencia_biometrica(
	id_asistencia_biometrica SERIAL PRIMARY KEY NOT NULL,
	id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
	id_puesto INTEGER NOT NULL REFERENCES puesto(id_puesto),
	tipo VARCHAR(20) NOT NULL CHECK (tipo IN('Entrada','Salida')),
	fecha date DEFAULT CURRENT_DATE NOT NULL,
	hora TIME DEFAULT CURRENT_TIME NOT NULL,
	estado_asistencia VARCHAR(20) NOT NULL CHECK (estado_asistencia IN ('A tiempo', 'Tarde', 'Temprana','Retraso minimo','Fuera de rango')),
	turno_asistencia VARCHAR (20) NOT NULL CHECK (turno_asistencia IN ('Mañana','Tarde','Noche')),
	vector_capturado TEXT NOT NULL,
	UNIQUE(id_empleado,fecha,tipo)
	
);

CREATE TABLE incidencia_asistencia(
	id_incidencia_asistencia SERIAL PRIMARY KEY NOT NULL,
	id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
    	id_periodo INTEGER NOT NULL REFERENCES periodo_empleado(id_periodo),
	fecha DATE NOT NULL,
	dia VARCHAR(30) NOT NULL CHECK (dia IN ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo')),
	tipo VARCHAR(30) NOT NULL CHECK (tipo IN ('Falta justificada','Falta no justificada', 'Licencia médica', 'Vacaciones', 'Suspensión','No laboral','Otra')),
	descripcion TEXT,
	UNIQUE (id_empleado,id_periodo,fecha)
);

CREATE TABLE historial_laboral(
	id_historial SERIAL PRIMARY KEY NOT NULL,
	id_empleado INTEGER NOT NULL REFERENCES empleado(id_empleado),
	empresa VARCHAR(30) NOT NULL,
	puesto_desempeñado VARCHAR(30) NOT NULL,
	fecha_inicio DATE NOT NULL,
	fecha_fin DATE NOT NULL,
	descripcion_tareas TEXT,
	referencia TEXT
  	CHECK (fecha_fin > fecha_inicio)
);

CREATE TABLE informacion_laboral(
	id_informacion_laboral SERIAL PRIMARY KEY NOT NULL,
  	id_departamento INTEGER NOT NULL REFERENCES departamento(id_departamento),
    	id_empleado INTEGER UNIQUE NOT NULL REFERENCES empleado(id_empleado),
	id_puesto INTEGER NOT NULL REFERENCES puesto(id_puesto),
	id_categoria INTEGER NOT NULL REFERENCES categoria(id_categoria),
	fecha_ingreso DATE NOT NULL,
	fecha_finalizacion DATE,
	turno VARCHAR(20) NOT NULL CHECK (turno IN ('Mañana', 'Tarde', 'Noche', 'Otro')),
	hora_inicio_turno TIME NOT NULL,
 	hora_fin_turno TIME NOT NULL,
	cantidad_horas_trabajo INTEGER NOT NULL,
	tipo_contrato VARCHAR(20) NOT NULL CHECK (tipo_contrato IN ('Tiempo indeterminado', 'Tiempo parcial','A plazo fijo', 'Por temporada','Eventual','Pasantia')),
	estado VARCHAR(20) NOT NULL CHECK(estado IN('Activo', 'Suspendido','Desafectado', 'Licencia','En formacion','Jubilado','Vacaciones')),
	tipo_semana_laboral VARCHAR(20) NOT NULL CHECK (tipo_semana_laboral IN ('Normal', 'Extendida', 'Completa'))
);

CREATE TABLE notificacion(
	id_notificacion SERIAL PRIMARY KEY NOT NULL,
	id_usuario INTEGER NOT NULL REFERENCES usuario(id_usuario),
	titulo VARCHAR(30) NOT NULL,
	mensaje TEXT,
	fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	leido BOOLEAN DEFAULT FALSE
);

CREATE TABLE evento_sistema(
	id_evento_sistema SERIAL PRIMARY KEY NOT NULL,
	id_usuario INTEGER NOT NULL REFERENCES usuario(id_usuario),
	tipo_evento VARCHAR(50) NOT NULL CHECK (tipo_evento IN ('Inicio_Sesion', 'Cierre_Sesion', 'Registro_Asistencia', 'Carga_Documento','Calculo de nomina','Otro')),
	fecha_evento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	descripcion text
);

CREATE TABLE error_sistema(
	id_error SERIAL PRIMARY KEY NOT NULL,
	id_usuario INTEGER NOT NULL REFERENCES usuario(id_usuario),
	origen VARCHAR(50) NOT NULL,
	tipo_error VARCHAR(50) NOT NULL,
	descripcion_error TEXT NOT NULL,
	dato_relacionado TEXT,
	fecha_error TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE VIEW calendario AS
SELECT 
    rj.id_empleado,
    rj.id_periodo,
    rj.fecha,
    rj.dia,
    rj.estado_jornada,
    rj.hora_entrada,
    rj.hora_salida,
    rj.horas_normales_trabajadas,
    rhe.cantidad_horas AS horas_extras,
    rj.observaciones AS descripcion
FROM 
    registro_jornada rj
LEFT JOIN 
    registro_hora_extra rhe ON rj.id_registro_jornada = rhe.id_registro_jornada

UNION ALL

SELECT 
    ia.id_empleado,
    ia.id_periodo,
    ia.fecha,
    ia.dia,
    ia.tipo AS estado_jornada,
    NULL AS hora_entrada,
    NULL AS hora_salida,
    NULL AS horas_trabajadas,
    NULL AS horas_extras,
    ia.descripcion
FROM 
    incidencia_asistencia ia;

CREATE OR REPLACE VIEW recibo_sueldo AS
SELECT 
    n.id_nomina,
    n.id_empleado,
    e.nombre,
    e.apellido,
    e.tipo_identificacion,
    e.numero_identificacion,
    p.nombre AS puesto,
    c.nombre_categoria AS categoria,
    d.nombre AS departamento,
    
    pe.periodo_texto AS periodo,
    n.fecha_de_pago,
    b.nombre AS banco,
    cu.numero_cuenta,
    n.salario_base,
    n.bono_presentismo,
    n.bono_antiguedad,
    n.horas_extra,

    n.descuento_jubilacion ,
    n.descuento_obra_social ,
    n.descuento_anssal ,
    n.descuento_ley_19032 ,
    n.impuesto_ganancias ,
    n.descuento_sindical ,
    n.sueldo_bruto,
    n.sueldo_neto
FROM 
        nomina n
JOIN 
        informacion_laboral il ON n.id_empleado = il.id_empleado
JOIN 
	empleado e ON n.id_empleado= e.id_empleado
JOIN 
	puesto p ON il.id_puesto = p.id_puesto
JOIN 
	categoria c ON il.id_categoria = c.id_categoria
JOIN 
	departamento d on il.id_departamento = d.id_departamento
JOIN 
	cuenta_bancaria cu on e.id_empleado = cu.id_empleado
JOIN
	banco b ON cu.id_banco = b.id_banco
JOIN
        periodo_empleado pe ON n.id_periodo = pe.id_periodo AND n.id_empleado = pe.id_empleado;


CREATE OR REPLACE FUNCTION obtener_o_crear_periodo_empleado(p_id_empleado INTEGER, p_fecha DATE) RETURNS INTEGER AS $$
DECLARE
    nombre_periodo VARCHAR(20);
    mes_es VARCHAR(20);
    id_de_periodo INTEGER;
BEGIN
		mes_es := CASE TO_CHAR(p_fecha, 'MM')
    		WHEN '01' THEN 'ENERO'
    		WHEN '02' THEN 'FEBRERO'
    		WHEN '03' THEN 'MARZO'
    		WHEN '04' THEN 'ABRIL'
    		WHEN '05' THEN 'MAYO'
    		WHEN '06' THEN 'JUNIO'
    		WHEN '07' THEN 'JULIO'
    		WHEN '08' THEN 'AGOSTO'
    		WHEN '09' THEN 'SEPTIEMBRE'
    		WHEN '10' THEN 'OCTUBRE'
    		WHEN '11' THEN 'NOVIEMBRE'
    		WHEN '12' THEN 'DICIEMBRE'
 	 END;

 	 nombre_periodo := mes_es || ' ' || TO_CHAR(p_fecha, 'YYYY');
         
		SELECT id_periodo INTO id_de_periodo 
		FROM periodo_empleado 
		WHERE id_empleado = p_id_empleado
		AND periodo_texto = nombre_periodo;

		IF NOT FOUND THEN
    			-- Insertar nuevo periodo_empleado
    			INSERT INTO periodo_empleado (
        		id_empleado,
        		periodo_fecha,
        		presentismo,
        		porcentaje_asistencia,
        		faltas_justificadas,
        		faltas_injustificadas,
        		periodo_texto,
        		valor_hora
    			) VALUES (
        		p_id_empleado,
        		DATE_TRUNC('month', p_fecha),
        		TRUE,
        		0,
        		0,
        		0,
        		nombre_periodo,
        		0  
    			)
    			RETURNING id_periodo INTO id_de_periodo;
		END IF;

		RETURN id_de_periodo;
END;

$$LANGUAGE plpgsql;



	CREATE OR REPLACE FUNCTION insertar_registro_jornada_hora_extra () RETURNS TRIGGER AS $$
	DECLARE
		hora_entrada TIME;
		horas_interval INTERVAL;
		horas_trabajadas INTEGER;
		estado_jornada TEXT;
		observaciones TEXT;
		horas_de_trabajo_estipuladas INTEGER;
		dia TEXT;
		nombre_periodo VARCHAR(20);
		mes_es VARCHAR(20);
		id_de_periodo INTEGER;
		horas_normales_trabajadas INTEGER;
		horas_extra_trabajadas INTEGER;
		id_jornada_insertada INTEGER;
		es_feriado BOOLEAN;
	BEGIN
		IF NEW.tipo = 'Salida' THEN
			-- Obtener hora de entrada
				SELECT hora 
				INTO hora_entrada
				FROM asistencia_biometrica 
				WHERE id_empleado = NEW.id_empleado 
				AND fecha = NEW.fecha
				AND tipo = 'Entrada'
				LIMIT 1;
	
		-- Obtener el día de la semana en español
			dia := CASE TO_CHAR(NEW.fecha, 'ID')
				WHEN '1' THEN 'Lunes'
				WHEN '2' THEN 'Martes'
				WHEN '3' THEN 'Miércoles'
				WHEN '4' THEN 'Jueves'
				WHEN '5' THEN 'Viernes'
				WHEN '6' THEN 'Sábado'
				WHEN '7' THEN 'Domingo'
			END;
	
		--Obtener el periodo
		
		id_de_periodo:=obtener_o_crear_periodo_empleado(NEW.id_empleado, NEW.fecha) ;
		
		-- Obtener horas estipuladas para el empleado
		SELECT cantidad_horas_trabajo 
		INTO horas_de_trabajo_estipuladas
		FROM informacion_laboral 
		WHERE id_empleado = NEW.id_empleado;
	
		-- Calcular intervalo de trabajo
		horas_interval := NEW.hora - hora_entrada;
	
		-- Calcular horas totales trabajadas
		horas_trabajadas := ROUND(EXTRACT(EPOCH FROM horas_interval) / 3600);
	
		--Calcular horas normales trabajadas sin horas extras
		IF horas_trabajadas > horas_de_trabajo_estipuladas THEN
			horas_extra_trabajadas:= horas_trabajadas - horas_de_trabajo_estipuladas;
			horas_normales_trabajadas:= horas_trabajadas - horas_extra_trabajadas;
		ELSE
			horas_extra_trabajadas:=0;
			horas_normales_trabajadas:=horas_trabajadas;		
	
		END IF;
		-- Determinar estado y observaciones
		IF horas_trabajadas > horas_de_trabajo_estipuladas THEN
				estado_jornada := 'Completa con horas extra';
				observaciones := 'Se completó la jornada laboral con éxito y con horas adicionales';
		ELSIF horas_trabajadas = horas_de_trabajo_estipuladas THEN
				estado_jornada := 'Completa';
				observaciones := 'Se completó la jornada laboral con éxito';
		ELSE
				estado_jornada := 'Incompleta';
				observaciones := 'Se realizó la jornada pero no se completaron las horas';
			END IF;
	
		-- Insertar en registro_jornada
		INSERT INTO registro_jornada (
		id_empleado,id_periodo,fecha, dia, hora_entrada, hora_salida, estado_jornada, horas_normales_trabajadas, observaciones
		)
		VALUES (
		NEW.id_empleado,id_de_periodo,NEW.fecha,dia, hora_entrada, NEW.hora, estado_jornada, horas_normales_trabajadas, observaciones
		)
		RETURNING id_registro_jornada INTO id_jornada_insertada;
	
	es_feriado := EXISTS (SELECT 1 FROM feriado WHERE fecha = NEW.fecha);

        -- Registrar horas extra si corresponde
        IF horas_extra_trabajadas > 0 THEN
            IF es_feriado OR dia = 'Domingo' THEN
                INSERT INTO registro_hora_extra (id_registro_jornada, cantidad_horas, tipo_hora_extra, observaciones)
                VALUES (id_jornada_insertada, horas_extra_trabajadas, '100%', 'Horas extra con recargo total (feriado o domingo)');

            ELSIF dia = 'Sábado' THEN
                IF NEW.hora > TIME '13:00' THEN
                    INSERT INTO registro_hora_extra (id_registro_jornada, cantidad_horas, tipo_hora_extra, observaciones)
                    VALUES (id_jornada_insertada, horas_extra_trabajadas, '100%', 'Horas extra con recargo total (sábado después de las 13:00)');
                ELSE
                    INSERT INTO registro_hora_extra (id_registro_jornada, cantidad_horas, tipo_hora_extra, observaciones)
                    VALUES (id_jornada_insertada, horas_extra_trabajadas, '50%', 'Horas extra con recargo del 50% (sábado antes de las 13:00)');
                END IF;

            ELSE
                INSERT INTO registro_hora_extra (id_registro_jornada, cantidad_horas, tipo_hora_extra, observaciones)
                VALUES (id_jornada_insertada, horas_extra_trabajadas, '50%', 'Horas extra con recargo del 50%(dia de semana)');
            END IF;
        END IF;
    END IF;
	
		RETURN NULL;
	END;
	$$ LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION insertar_dias_no_laborales_incidencia_asistencia() 
RETURNS TRIGGER AS $$
DECLARE
    tipo_semana TEXT;
    fecha_sabado DATE;
    fecha_domingo DATE;
    nombre_periodo VARCHAR(20);
    mes_es VARCHAR(20);
    id_de_periodo_sabado INTEGER;
	id_de_periodo_domingo INTEGER;
BEGIN
    IF NEW.dia = 'Viernes' THEN 
       SELECT tipo_semana_laboral INTO tipo_semana FROM informacion_laboral WHERE id_empleado = NEW.id_empleado;
        
        fecha_sabado := NEW.fecha + INTERVAL '1 day';
        fecha_domingo := NEW.fecha + INTERVAL '2 days';
		id_de_periodo_sabado:=obtener_o_crear_periodo_empleado(NEW.id_empleado, fecha_sabado) ;
		id_de_periodo_domingo:=obtener_o_crear_periodo_empleado(NEW.id_empleado, fecha_domingo);
        
        IF tipo_semana = 'Normal' THEN
            -- Inserta sábado
            INSERT INTO incidencia_asistencia (id_empleado,id_periodo,fecha, dia, tipo, descripcion)
            VALUES (NEW.id_empleado, id_de_periodo_sabado,fecha_sabado, 'Sábado', 'No laboral', 'No corresponde debido a su tipo de semana laboral');
            -- Inserta domingo
            INSERT INTO incidencia_asistencia (id_empleado,id_periodo, fecha, dia, tipo, descripcion)
            VALUES (NEW.id_empleado,id_de_periodo_domingo, fecha_domingo, 'Domingo', 'No laboral', 'No corresponde debido a su tipo de semana laboral');
        
        ELSIF tipo_semana = 'Extendida' THEN
            -- Inserta solo domingo
            INSERT INTO incidencia_asistencia (id_empleado,id_periodo, fecha, dia, tipo, descripcion)
            VALUES (NEW.id_empleado,id_de_periodo_domingo, fecha_domingo, 'Domingo', 'No laboral', 'No corresponde debido a su tipo de semana laboral');
        
        ELSIF tipo_semana = 'Completa' THEN
            -- No hacer nada
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION actualizar_vigencia_fin_salario() RETURNS TRIGGER AS $$
DECLARE

fecha_fin_vigencia DATE;

BEGIN

	-- Obtener el día anterior al inicio del nuevo registro
    SELECT (NEW.fecha_inicio - INTERVAL '1 day')::DATE INTO fecha_fin_vigencia;
	
	UPDATE salario_base SET fecha_fin = fecha_fin_vigencia
	WHERE id_puesto = NEW.id_puesto AND id_departamento = NEW.id_departamento 
	AND id_categoria = NEW.id_categoria
  	AND fecha_fin IS NULL;
	  
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION actualizar_presentismo_empleado () RETURNS TRIGGER AS $$
DECLARE

BEGIN
	IF NEW.tipo='Falta no justificada' THEN
		UPDATE periodo_empleado
		SET presentismo = FALSE
		WHERE id_periodo = NEW.id_periodo
  		AND presentismo = TRUE;
	END IF;
RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insertar_registro_jornada_hora_extra_trg
AFTER INSERT ON asistencia_biometrica
FOR EACH ROW
EXECUTE FUNCTION insertar_registro_jornada_hora_extra();

CREATE TRIGGER insertar_dias_no_laborales_desde_incidencia_trg
AFTER INSERT ON incidencia_asistencia
FOR EACH ROW
EXECUTE FUNCTION insertar_dias_no_laborales_incidencia_asistencia();

CREATE TRIGGER insertar_dias_no_laborales_desde_registro_trg
AFTER INSERT ON registro_jornada
FOR EACH ROW
EXECUTE FUNCTION insertar_dias_no_laborales_incidencia_asistencia();

CREATE TRIGGER actualizar_vigencia_fin_salario_trg
BEFORE INSERT ON salario_base
FOR EACH ROW
EXECUTE FUNCTION actualizar_vigencia_fin_salario();

CREATE TRIGGER actualizar_presentismo_empleado_trg
AFTER INSERT ON incidencia_asistencia
FOR EACH ROW
EXECUTE FUNCTION actualizar_presentismo_empleado();




