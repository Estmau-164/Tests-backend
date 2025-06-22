--Roles
INSERT INTO rol (
  id_rol, nombre, fecha_creacion, online_login, offline_login, ver_datos_personales,
  editar_datos_personales, ver_datos_laborales, agregar_datos_laborales, editar_datos_laborales,
  agregar_empleado, ver_registro_asistencia, ver_informacion_bancaria, editar_informacion_bancaria,
  ingresar_asistencia, ingresar_inasistencia, ver_historial_nominas, calcular_nomina_manualmente,
  calcular_nomina_automaticamente, agregar_concepto, agregar_departamento, agregar_puesto,
  agregar_categoria, agregar_salario_con_vigencia, ver_vista_previa_recibo_sueldo,
  descargar_recibo_sueldo, ver_reportes, cerrar_sesion, descripcion
) VALUES
(1, 'Empleado', '2025-06-01', TRUE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, FALSE, TRUE, 'Rol que corresponde al empleado comun, tiene permisos asociados a lectura y muy limitada escritura/modificacion'),
(2, 'Administrador_RRHH', '2025-06-01', TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, 'El administrador de recursos humanos tiene todos los permisos de escritura/lectura/modificacion/actualizacion posibles'),
(3, 'Supervisor', '2025-06-01', TRUE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, TRUE, 'El supervisor es el rol el cual tiene permisos de lectura y escritura pero mas que nada asociado a los empelados para poder monitorearlos correctamente'),
(4, 'Analista_de_datos', '2025-06-01', TRUE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, TRUE, TRUE, TRUE, TRUE, 'El analista de datos tiene los permisos de lectura y escritura parecidos a los del supervisor nomas que este esta mas enfocado a lo analitico, graficos, reportes de metricas en general');