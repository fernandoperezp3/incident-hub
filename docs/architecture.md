# Arquitectura

## Contexto

IT Incident Hub reúne reportes de soporte que antes quedaban dispersos. La solución se ejecuta localmente y permite demostrar funcionalidad y entrega continua sin un servicio de nube obligatorio.

## Componentes

```text
Navegador ── HTTP ──> servidor Python (estáticos + API REST) ──> SQLite
                         localhost:8000                         database/incidents.db
```

- **Frontend:** HTML, CSS y JavaScript sin compilación; sirve desde el mismo origen que la API.
- **Backend:** servidor HTTP de Python y endpoints REST.
- **Datos:** SQLite, inicialización automática y datos de demostración.
- **CI:** GitHub Actions compila, ejecuta pruebas, audita el inventario de dependencias y publica un ZIP.

El stack de referencia PostgreSQL/React del enunciado es opcional: permite tecnologías equivalentes documentadas. SQLite y la interfaz sin framework reducen requisitos para que el prototipo sea fácil de ejecutar. Una versión desplegable de producción requeriría evaluar PostgreSQL, autenticación, autorización, CORS restringido, observabilidad y secretos de despliegue.

## Entidades

- **Incident:** título, descripción, categoría, prioridad, reportante, técnico, estado, fechas.
- **Activity:** incidente, autor, mensaje y fecha; conserva asignaciones, transiciones y comentarios.

## Decisiones

| Decisión | Motivo | Consecuencia |
|---|---|---|
| Un único repositorio | Aclaración vigente del ingeniero | UI, API, datos, pruebas y CI avanzan en un solo PR stream. |
| GitHub Issues/Projects | No se dispone de Azure y el repo vive en GitHub | Sustituye el tablero de Azure con trazabilidad Issue → rama → commit → PR → Actions. |
| Python estándar + SQLite | Ejecución local sencilla y sin servicios | Adecuado para demo individual; no se plantea como infraestructura de producción. |

