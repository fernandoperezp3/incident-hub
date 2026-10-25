# Seguridad y gestión de dependencias

## Controles incluidos

- Runtime sin paquetes externos; `requirements.txt` registra el inventario intencionalmente vacío.
- Consultas SQL parametrizadas y restricciones CHECK para estados y prioridades.
- Datos SQLite y archivos `.env` excluidos por Git.
- GitHub Actions usa permisos mínimos de lectura y ejecuta `pip-audit` contra el inventario declarado.
- La API limita cuerpos JSON a 1 MiB y valida que cada carga sea un objeto.
- Las listas de incidentes usan paginación con máximo de 100 registros por solicitud.
- No se solicitan ni almacenan tokens en el código.

## Riesgos de la demostración

El prototipo no autentica usuarios y no está diseñado para exposición pública. Usar solo datos ficticios. Antes de desplegar fuera de localhost: añadir autenticación y autorización por rol, política de retención, logging y CORS estricto; usar base de datos administrada y respaldos; guardar secretos en GitHub Environments; revisar la configuración del host.

## Registro de cinco deudas técnicas

| ID | Hallazgo / riesgo | Severidad | Decisión | Estado / evidencia |
|---|---|---|---|---|
| TD-01 | No hay autenticación ni autorización. | Alta | Aceptado solo para demo local; no usar datos reales. | Abierto. |
| TD-02 | SQLite no está preparado para concurrencia y escala de producción. | Media | Mantener para demo; evaluar PostgreSQL antes de un despliegue. | Abierto; decisión en [architecture.md](architecture.md). |
| TD-03 | La lista de incidentes no tenía paginación. | Media | Limitar resultados y entregar metadatos de siguiente página. | Resuelto en [PR #37](https://github.com/fernandoperezp3/incident-hub/pull/37); CI verde en [run 39819695858](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819695858). |
| TD-04 | La API no limitaba el tamaño del cuerpo ni validaba el tipo JSON raíz. | Media | Limitar a 1 MiB y requerir un objeto JSON. | Resuelto en [PR #38](https://github.com/fernandoperezp3/incident-hub/pull/38); CI verde en [run 39819966156](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819966156). |
| TD-05 | Mantener disponible el runner self-hosted de Windows para la demostración. | Media | Runner propio de GitHub Actions; no se usa Azure. | Configurado y ejecutado correctamente; [Issue #33](https://github.com/fernandoperezp3/incident-hub/issues/33) cerrado y [run 39878187941](https://github.com/fernandoperezp3/incident-hub/actions/runs/39878187941) exitoso. |

## Correcciones surgidas en la primera ejecución de CI

La prueba inicial reveló estado de base temporal compartido entre casos y datos de muestra que asumían un ID fijo. El pipeline también usaba nombres distintos para el ZIP y el artefacto. Se corrigieron con aislamiento por prueba, IDs generados y ruta alineada en [PR #2](https://github.com/fernandoperezp3/incident-hub/pull/2), que enlaza el run rojo inicial y el verde [39817414741](https://github.com/fernandoperezp3/incident-hub/actions/runs/39817414741).

El inventario de runtime no declara dependencias externas. La ejecución real de `pip-audit` forma parte del CI y sus resultados están registrados en los runs enlazados.
