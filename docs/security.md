# Seguridad y gestión de dependencias

## Controles incluidos

- Runtime sin paquetes externos; `requirements.txt` registra el inventario intencionalmente vacío.
- Consultas SQL parametrizadas y restricciones CHECK para estados y prioridades.
- Datos SQLite y archivos `.env` excluidos por Git.
- GitHub Actions usa permisos mínimos de lectura y ejecuta `pip-audit` contra el inventario declarado.
- No se solicitan ni almacenan tokens en el código.

## Riesgos de la demostración

El prototipo no autentica usuarios y no está diseñado para exposición pública. Usar solo datos ficticios. Antes de desplegar fuera de localhost: añadir autenticación y autorización por rol, límites de solicitudes y tamaño, política de retención, logging y CORS estricto; usar base de datos administrada y respaldos; guardar secretos en GitHub Environments; revisar la configuración del host.

## Registro de deuda técnica

| ID | Hallazgo / riesgo | Severidad | Decisión | Estado / evidencia |
|---|---|---|---|---|
| TD-01 | No hay autenticación ni autorización. | Alta | Aceptado solo para demo local; no usar datos reales. | Abierto. |
| TD-02 | SQLite no está preparado para concurrencia y escala de producción. | Media | Mantener para demo; evaluar PostgreSQL antes de un despliegue. | Abierto; decisión en [architecture.md](architecture.md). |
| TD-03 | Las pruebas compartían estado de base temporal y dependían de IDs sembrados. | Media | Aislar datos por prueba y obtener IDs generados. | Resuelto en [PR #2](https://github.com/fernandoperezp3/incident-hub/pull/2); CI verde enlazado allí. |
| TD-04 | Nombre del archivo ZIP del pipeline no coincidía con la ruta de carga. | Media | Usar SHA completo en nombre y ruta del artefacto. | Resuelto en [PR #2](https://github.com/fernandoperezp3/incident-hub/pull/2); upload artifact verde. |
| TD-05 | No existe runner self-hosted registrado ni ejecución de evidencia. | Media | Registrar runner de GitHub en la computadora propia; no usar Azure. | Pendiente; seguimiento en [Issue #33](https://github.com/fernandoperezp3/incident-hub/issues/33). |

El pipeline ejecuta `pip-audit` en cada PR. El inventario base no declara dependencias externas; el resultado real se encuentra en el run de CI enlazado por PR #2.
