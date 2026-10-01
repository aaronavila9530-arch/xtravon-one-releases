# XTRAVON ONE | GRAIN CONTROL

Manual operativo detallado para supervisores, operadores de patio, despacho, choferes y clientes.

Este manual explica el flujo completo de operación. La ayuda integrada en la app usa el mismo criterio: responder dudas con pasos concretos, sin depender de P.O.R.T.I.A.

## 1. Logueo

![Logo XTRAVON](../assets/XTRAVON_seal_round_transparent.png)

1. Abra XTRAVON ONE desde el icono de la aplicación.
2. Espere a que finalice la pantalla de carga.
3. Seleccione el perfil:
   - Supervisor.
   - Operador patio.
   - Cliente.
   - Chofer.
4. En producción, cada usuario debe iniciar sesión con credenciales reales.
5. Valide que el menú visible corresponda al rol.

Validaciones:

- Operador patio solo debe ver Lector QR Patio y SOF.
- Chofer solo debe ver su portal de guías/QR.
- Cliente solo debe ver su portal, informes y consultas autorizadas.

## 2. Apertura de buque

1. Ingrese a Operaciones Buque.
2. Presione la opción de nueva operación.
3. Digite el nombre del buque.
4. Seleccione fecha de inicio.
5. Agregue productos con el botón `+`.
6. Defina capacidades por bodega en MT.
7. Si una bodega está partida:
   - Use particiones.
   - Registre tonelaje por partición.
   - Mantenga la suma igual a la capacidad total de esa bodega.
8. Revise la silueta del buque.
9. Presione Abrir operación.
10. Confirme que la operación quede en estado ABIERTA.

No cierre una operación hasta confirmar descarga, documentos, SOF y autorizaciones.

## 3. Stowage plan

El stowage plan debe registrar:

- Bodega.
- Producto.
- Capacidad MT.
- Particiones.
- Cliente o grupo si aplica.
- Observaciones operativas.

Regla:

Si una bodega tiene más de un producto o cliente, debe existir partición visible para evitar mezclar descarga, cuota y reporte.

## 4. Cuotas por cliente

1. En Operaciones Buque, seleccione la operación.
2. Agregue cliente.
3. Agregue cuota.
4. Seleccione unidad: KG, LB o MT.
5. Use `+` para agregar N clientes.
6. Use `-` para eliminar líneas.
7. Presione Crear cuotas.
8. Presione Cargar cuotas activas para validar.

Las cuotas alimentan:

- Avance por cliente.
- Sobrecuota.
- Pendiente de descarga.
- Alertas.
- Informes.

## 5. Carga inicial de guías y choferes

1. Ingrese a Carga de Boletas.
2. Presione Buscar operación activa.
3. Presione Abrir Template.
4. Complete Excel:
   - Guía.
   - Empresa/cliente.
   - Buque.
   - Fecha.
   - Producto.
   - Chofer.
   - Placa.
   - Bodega si aplica.
   - Embarque si aplica.
5. Guarde el Excel.
6. Presione Cargar Excel.
7. Presione Cargar Tabla para consultar.

Regla:

La carga inicial pertenece a la operación abierta y queda aprobada automáticamente. No debe pasar por Aprobaciones porque forma parte del arranque planificado.

## 6. Guías extraordinarias y aprobaciones

Use Aprobaciones solo cuando se carguen guías fuera de la carga inicial.

1. Abra template de aprobaciones.
2. Complete guías extraordinarias.
3. Cargue Excel.
4. Presione Ver datos cargados.
5. Filtre si aplica.
6. Marque registros.
7. Seleccione acción:
   - Aprobar.
   - Rechazar.
   - Seleccionar todo.
   - Desmarcar todo.
8. Agregue comentario si rechaza o necesita evidencia.
9. Al aprobar, el sistema genera QR y pass hatch.

## 7. Despacho de viajes

Despacho controla asignación, continuidad y reasignación.

1. Ingrese a Despacho de Viajes.
2. Busque operación activa.
3. Revise tableros:
   - Solicitudes de nuevo viaje.
   - Guías asignadas.
   - Primer escaneo.
   - Segundo escaneo.
   - Tercer escaneo.
   - Guías completadas.
   - Choferes disponibles.
   - Bloqueos activos.
4. Para asignar:
   - Seleccione chofer.
   - Seleccione placa.
   - Seleccione cliente.
   - Seleccione producto.
   - Presione asignar.
5. El sistema genera o habilita QR.
6. El QR queda visible en la app del chofer.
7. Opcionalmente se envía por WhatsApp o correo si las variables están configuradas.

Regla crítica:

El ERP puede proponer, pero despacho confirma. No debe existir autoasignación ciega.

## 8. Portal chofer

El chofer solo debe ver:

- Guía activa.
- QR activo.
- Empresa.
- Producto.
- Chofer.
- Viajes asignados.
- Viajes pendientes.
- Peso acumulado.

El chofer no debe ver:

- Pass hatch.
- Información completa del backend.
- Datos de otros choferes.
- Acciones de supervisor.

Al completar tercer escaneo:

1. La guía actual se archiva.
2. La app pregunta si desea continuar.
3. Si responde sí, confirma la decisión.
4. Si tiene guías asignadas, muestra el siguiente QR.
5. Si responde no, sus guías pendientes pasan a despacho para reasignación manual.

## 9. Lector QR Patio

Primer escaneo:

- Ficha.
- Peso vacío.

Segundo escaneo:

- Número de tolva.

Tercer escaneo:

- Peso lleno.
- Marchamos.

Marchamos:

- Use `+` para agregar marchamos.
- Use `-` para eliminar marchamos.
- Cada marchamo se guarda como entrada individual y también consolidado para trazabilidad.

Offline:

Si no hay señal, el handheld guarda en memoria local y reintenta enviar automáticamente al recuperar conexión.

## 10. SOF

1. Ingrese a SOF.
2. La operación abierta debe quedar seleccionada por defecto.
3. Seleccione fecha.
4. Ingrese hora desde y hora hasta.
5. Seleccione tipo/subcategoría.
6. Seleccione bodega si aplica.
7. Escriba evento.
8. Guarde.

SOF también funciona offline en app/handheld y sincroniza al volver red.

## 11. Centro Ejecutivo

1. Ingrese a Centro Ejecutivo.
2. Busque operación.
3. Cargue filtros.
4. Filtre por:
   - Empresa.
   - Guía.
   - Producto.
   - Chofer.
   - Placa.
5. Presione Generar datos.
6. Revise:
   - KPIs.
   - Silueta del buque.
   - Bodegas.
   - Cuotas vs descargado.
   - Duración por camión.
   - Tendencia diaria.
   - Alertas.

Los datos no deben cargar automáticamente para evitar lag.

## 12. Informes

Tipos sugeridos:

- Resumen ejecutivo por buque.
- SOF.
- Cuotas vs descargado.
- Descarga por bodega.
- Alertas operativas.
- Productividad por camión.
- Diferencias documentales.

Formatos:

- PDF.
- Excel.
- Word.
- CSV.

## 13. P.O.R.T.I.A

P.O.R.T.I.A es el asistente operativo.

Activación:

- Oye Portia.
- Hola Portia.
- Portia estás ahí.
- Hey Portia.

Desactivación:

- Es todo Portia.
- Desconéctate Portia.
- Silencio Portia.

Puede consultar:

- Riesgos.
- SOF.
- Duración estimada.
- Clientes atrasados.
- Bodegas críticas.
- Clima.
- Calados.
- Ubicación AIS si existe API configurada.

## 14. Ayuda / Q&A

La pantalla Ayuda / Q&A responde con base en este manual.

Ejemplos:

- ¿Cómo abro un buque?
- ¿Cómo apruebo guías?
- ¿Cómo escaneo offline?
- ¿Cómo reasigno un viaje?
- ¿Cómo cargo SOF?

Esta ayuda no sustituye a P.O.R.T.I.A. Es una guía de uso paso a paso.
