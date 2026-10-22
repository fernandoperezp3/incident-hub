# Seguridad y gestión de dependencias

## Controles incluidos

- Runtime sin paquetes externos; `requirements.txt` registra el inventario intencionalmente vacío.
- SQL parametrizado para filtros y cambios; restricciones CHECK para estados y prioridades.
- Datos SQLite y archivos `.env` ignorados por Git.
- Workflow con permisos mínimos de lectura; dependency review corre en PR.
- No se solicitan ni almacenan tokens en el código.

## Riesgos de la demostración

Este prototipo no autentica usuarios y el servidor no está diseñado para exposición pública. Solo usar datos ficticios. Antes de desplegar fuera de localhost: añadir autenticación y autorización por rol, límites de solicitudes/tamaño, política de retención, logging y CORS estricto; usar una base de datos administrada y respaldos; guardar secretos en GitHub Environments; revisar la configuración del host.

## Registro de deuda técnica

| ID | Hallazgo / riesgo | Severidad | Decisión | Estado / evidencia |
|---|---|---|---|---|
| TD-01 | No hay autenticación/autorización. | Alta | Aceptado solo para demo local; crear Issue si se planea despliegue. | Abierto; no usar datos reales. |
| TD-02 | SQLite no está preparado para concurrencia/escala de producción. | Media | Mantener para demo; evaluar PostgreSQL para despliegue. | Abierto; decisión en architecture.md. |
| TD-03 | No hay paginación para listas ni bitácora. | Media | Implementar si el volumen de datos crece. | Abierto; verificar límite razonable durante estabilización. |
| TD-04 | No hay registro central de auditoría ni retención definida. | Media | Evaluar antes de operar con datos reales. | Abierto. |
| TD-05 | No existe despliegue con ambiente de staging/rollback automatizado. | Media | En esta etapa preparar release manual controlado. | Abierto; plan en release.md. |

La consigna solicita identificar cinco deudas y resolver al menos dos mediante trabajo trazable. Estos cinco hallazgos son riesgos iniciales del diseño, no se reportan como deuda resuelta. Al iniciar la fase de hardening, elegir dos mejoras acotadas, crear Issues, completar PRs y reemplazar su estado con enlaces reales. No inventar resultados de análisis de paquetes: el runtime base no declara dependencias externas; guardar el resultado de `pip-audit` de CI.
