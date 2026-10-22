# API REST

Base local: `http://localhost:8000/api`. Las solicitudes y respuestas usan JSON UTF-8.

| Método | Ruta | Uso |
|---|---|---|
| GET | `/health` | Estado del servicio. |
| GET | `/incidents` | Lista; filtros opcionales `status`, `priority`, `category`, `technician`. |
| GET | `/incidents/{id}` | Detalle y bitácora. |
| POST | `/incidents` | Crea incidente con `title`, `description`, `category`, `priority`, `reporter`. |
| PATCH | `/incidents/{id}` | Actualiza `status` y/o `technician`. |
| POST | `/incidents/{id}/activity` | Agrega `author` y `message` a la bitácora. |
| GET | `/metrics` | Totales y distribución por categoría y técnico. |

Prioridades válidas: `BAJA`, `MEDIA`, `ALTA`, `CRITICA`. Estados válidos: `NUEVO`, `ASIGNADO`, `EN_PROCESO`, `RESUELTO`, `CERRADO`. Errores devuelven un objeto `{ "error": "..." }` y un código HTTP 4xx.
