# IT Incident Hub

Portal web para registrar, asignar y seguir incidentes de soporte de TI. Este proyecto integrador demuestra un flujo DevOps reproducible en **un solo repositorio de GitHub**.

## Estado del proyecto

Versión inicial de trabajo: `0.1.0`. El alcance vigente usa GitHub Issues/Projects y GitHub Actions. La mención del documento original a tres repositorios y Azure Boards/Pipelines corresponde a una instrucción anterior; el ingeniero confirmó que se entregará un repositorio y el estudiante no cuenta con Azure.

## Requisitos

- Python 3.10 o posterior (solo biblioteca estándar).
- Navegador moderno.
- Git y una cuenta de GitHub para publicar el repositorio.

## Ejecutar localmente

```powershell
python backend/app.py
```

Abrir <http://localhost:8000>. En el primer inicio se crea `database/incidents.db` con incidentes de demostración. La base local queda excluida de Git. Para cambiar puerto o ubicación de datos, configurar `PORT` o `INCIDENT_DB`.

## Funcionalidad

- Alta y consulta de incidentes, prioridad y categorías.
- Asignación de técnico y flujo `NUEVO → ASIGNADO → EN_PROCESO → RESUELTO → CERRADO`.
- Bitácora por incidente, filtros y búsqueda.
- Indicadores de abiertos, cerrados, críticos y distribución.
- API documentada en [docs/api.md](docs/api.md).

## Comprobaciones locales

```powershell
python -m compileall -q backend tests
python -m unittest discover -s tests -v
```

GitHub Actions ejecuta estas comprobaciones en Pull Requests y en `main`, revisa cambios de dependencias y publica un ZIP como artefacto de CI.

## Estructura

```text
backend/                 API HTTP y persistencia SQLite
frontend/                interfaz web
database/                datos locales (ignorados por Git)
tests/                   comprobaciones automatizadas de API
docs/                    arquitectura, backlog y operación
.github/workflows/       integración continua
```

## Flujo GitHub

1. Crear un Issue desde una historia de usuario o reporte de defecto.
2. Trabajar en una rama `feature/<issue>-resumen`, `fix/<issue>-resumen` o `refactor/<issue>-resumen`.
3. Vincular commits y PR al Issue con `Closes #N`; dejar `main` estable.
4. Solicitar revisión, atender observaciones y exigir CI verde antes de integrar.
5. Crear tags SemVer y Releases de GitHub siguiendo [la guía de release](docs/release.md).

## Limitaciones del prototipo

La aplicación es una demostración académica local. SQLite facilita ejecutar el proyecto sin servicios externos; no incluye autenticación ni debe exponerse a Internet con datos reales. Decisiones y trabajos pendientes están en `docs/`.

## Responsables

Proyecto individual: Mario Pérez. Toda contribución verificable se hará con su cuenta GitHub; no se crearán usuarios adicionales.
