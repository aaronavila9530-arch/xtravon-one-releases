# XTRAVON ONE - Auditoria de Consolidacion Operativa

Fecha: 2026-05-21

## Cambios aplicados

- Se elimino codigo muerto duplicado en `main.py`.
- Se centralizo la generacion de hash QR en `backend/services/qr_security.py`.
- Se agrego un pool de conexiones PostgreSQL en `backend/database.py`.
- Se agrego timeout/cancelacion al cliente API movil para evitar esperas indefinidas cuando el backend no responde.
- Se verifico compilacion Python de backend/frontend desktop.
- Se verifico export Android de Expo.

## Riesgos detectados

- `main.py` sigue siendo demasiado grande. Debe convertirse gradualmente en un shell de navegacion y mover pantallas a modulos.
- La entrega QR por WhatsApp requiere una URL publica de media o integracion formal con proveedor. Si no existe, solo puede mandar texto/link.
- `QR_SECRET` debe existir en Railway. El valor por defecto solo debe usarse en desarrollo local.
- Hay flujos relacionados que todavia deben compartir servicios comunes: filtros, aprobaciones, reasignacion, despacho y entrega QR.
- El movil debe conservar llamadas automaticas solo para sincronizacion offline operativa.

## Siguiente consolidacion recomendada

1. Crear `backend/services/operation_filters.py` para alimentar todos los combobox desde una sola fuente.
2. Crear `backend/services/dispatch_service.py` para asignar, liberar, cancelar, bloquear y auditar guias.
3. Crear `backend/services/qr_delivery.py` para envio por carpeta, correo y WhatsApp con la misma regla de seleccion.
4. Separar desktop en modulos por pantalla y dejar `main.py` como contenedor.
5. Agregar idempotencia a aprobaciones, reasignaciones y entrega QR para evitar duplicados por reintentos.
6. Hacer RBAC obligatorio en backend, no solo visual en frontend.
