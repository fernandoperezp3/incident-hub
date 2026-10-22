# Backlog inicial en GitHub Projects

Los identificadores siguientes son claves de planificación, no números de Issue emitidos por GitHub. Al crear los Issues, registrar su número real aquí y mantener el vínculo. Responsable inicial: Mario Pérez. Estimación en horas de trabajo.

## Epics y Features

| Clave | Tipo | Título | Prioridad | Estimación | Estado |
|---|---|---|---|---:|---|
| E1 | Epic | Gestión operativa de incidentes | P1 | 20 h | En curso |
| F1 | Feature | Registro y consulta | P1 | 6 h | En curso |
| F2 | Feature | Asignación, estados y bitácora | P1 | 7 h | En curso |
| E2 | Epic | Entrega continua y lanzamiento | P1 | 22 h | En curso |
| F3 | Feature | Tablero, calidad y seguridad | P1 | 9 h | En curso |
| F4 | Feature | Versionado y release controlado | P2 | 7 h | Pendiente |

## Historias de usuario

| Clave | Feature | Historia | Prioridad | Estimación | Estado |
|---|---|---|---|---:|---|
| US1 | F1 | Como usuario, quiero registrar un incidente con sus datos básicos para reportar una falla. | P1 | 3 h | En curso |
| US2 | F1 | Como soporte, quiero consultar y filtrar incidentes para encontrar trabajo pendiente. | P1 | 3 h | En curso |
| US3 | F2 | Como coordinador, quiero asignar un técnico para que cada caso tenga responsable. | P1 | 2 h | En curso |
| US4 | F2 | Como técnico, quiero cambiar el estado del incidente para reflejar su avance. | P1 | 2 h | En curso |
| US5 | F2 | Como equipo, quiero registrar comentarios para conservar el historial de atención. | P1 | 3 h | En curso |
| US6 | F3 | Como coordinador, quiero ver indicadores para entender el volumen y la prioridad. | P1 | 3 h | En curso |
| US7 | F3 | Como revisor, quiero que PRs ejecuten validaciones y análisis de dependencias. | P1 | 3 h | En curso |
| US8 | F4 | Como responsable de release, quiero etiquetar y publicar versiones con una guía de reversión. | P2 | 3 h | Pendiente |

## Tareas

| Clave | Historia | Trabajo | Prioridad | Est. | Estado |
|---|---|---|---|---:|---|
| T01 | US1 | Definir esquema y validación de incidentes | P1 | 1 h | En curso |
| T02 | US1 | Crear formulario y endpoint de alta | P1 | 2 h | En curso |
| T03 | US2 | Listar y ordenar incidentes | P1 | 1 h | En curso |
| T04 | US2 | Implementar filtros y búsqueda | P1 | 2 h | En curso |
| T05 | US3 | Implementar asignación de técnico | P1 | 1 h | En curso |
| T06 | US3 | Mostrar responsable en el tablero | P1 | 1 h | En curso |
| T07 | US4 | Validar transiciones de estado | P1 | 1 h | En curso |
| T08 | US4 | Añadir controles de flujo en detalle | P1 | 1 h | En curso |
| T09 | US5 | Persistir comentarios y eventos | P1 | 2 h | En curso |
| T10 | US5 | Presentar bitácora ordenada | P1 | 1 h | En curso |
| T11 | US6 | Calcular métricas de operación | P1 | 1 h | En curso |
| T12 | US6 | Mostrar gráficos por categoría/técnico | P1 | 2 h | En curso |
| T13 | US7 | Crear workflow de validación de PR | P1 | 1 h | En curso |
| T14 | US7 | Añadir pruebas, revisión de dependencias y artefacto | P1 | 2 h | En curso |
| T15 | US8 | Documentar SemVer, ambientes y promoción | P2 | 2 h | Pendiente |
| T16 | US8 | Preparar checklist de publicación y reversión | P2 | 1 h | Pendiente |
| T17 | US7 | Configurar y documentar un runner autohospedado de GitHub Actions | P2 | 2 h | Pendiente |

## Evidencia y seguimiento

Crear un GitHub Project con estados `Backlog`, `Ready`, `In progress`, `In review`, `Done`; campos `Priority`, `Estimate (h)`, `Owner` y `Feature`. Asignar Mario Pérez a los Items, registrar sus Issues reales y vincular cada PR con `Closes #N`. La tabla muestra el plan inicial; actualizar estados, estimaciones y enlaces al trabajar.
