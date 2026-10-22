# IT Incident Hub

Portal web para registrar, asignar y dar seguimiento a incidentes de soporte de TI. Proyecto integrador con un repositorio público: [fernandoperezp3/incident-hub](https://github.com/fernandoperezp3/incident-hub).

## Alcance

El ingeniero confirmó que la entrega se realizará en un solo repositorio GitHub y que no se usará Azure. El plan de trabajo está en [GitHub Issues](https://github.com/fernandoperezp3/incident-hub/issues) y sus relaciones en [docs/backlog.md](docs/backlog.md).

## Requisitos

- Python 3.10 o posterior (biblioteca estándar).
- Navegador moderno.

## Ejecutar localmente

```powershell
python backend/app.py
```

Abrir <http://localhost:8000>. En el primer inicio se crea `database/incidents.db` con incidentes de demostración. La base local queda excluida de Git. Para cambiar puerto o ubicación, configurar `PORT` o `INCIDENT_DB`.

## Funcionalidad

- Alta y consulta de incidentes, prioridad y categorías.
- Asignación de técnico y flujo `NUEVO → ASIGNADO → EN_PROCESO → RESUELTO → CERRADO`.
- Bitácora por incidente, filtros y búsqueda.
- Indicadores de abiertos, cerrados, críticos y distribución.
- API documentada en [docs/api.md](docs/api.md).

## Comprobaciones

```powershell
python -m compileall -q backend tests
python -m unittest discover -s tests -v
```

GitHub Actions ejecuta compilación, pruebas automatizadas, `pip-audit` y empaquetado ZIP en PRs y cambios a `main`. La validación verde y el artefacto de CI están enlazados desde [PR #2](https://github.com/fernandoperezp3/incident-hub/pull/2). El runtime no declara paquetes de terceros.

## Estructura

```text
backend/                 API HTTP y persistencia SQLite
frontend/                interfaz web
database/                datos locales (ignorados por Git)
tests/                   pruebas automatizadas de API
docs/                    arquitectura, backlog y operación
.github/workflows/       integración continua
```

## Flujo de trabajo

1. Tomar una tarea desde [Issues](https://github.com/fernandoperezp3/incident-hub/issues).
2. Crear una rama `feature/<issue>-resumen`, `fix/<issue>-resumen` o `docs/<issue>-resumen`.
3. Abrir PR hacia `main`, vincular el Issue con `Closes #N` y esperar el CI verde.
4. Registrar revisión técnica y merge en el historial del PR.
5. Preparar el tag y Release según [docs/release.md](docs/release.md).

## Límites

Es una demostración académica local: no incluye autenticación y no debe exponerse a Internet ni usarse con datos reales. Deuda técnica y riesgos están descritos en [docs/security.md](docs/security.md). El alta y la ejecución del runner self-hosted quedan como pendiente porque requiere que una computadora del estudiante ejecute el servicio de GitHub Actions; ver [Issue #33](https://github.com/fernandoperezp3/incident-hub/issues/33).

## Responsable

Proyecto individual: Mario Pérez (@fernandoperezp3).
