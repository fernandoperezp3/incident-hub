# Backlog del proyecto

Repositorio público único: [fernandoperezp3/incident-hub](https://github.com/fernandoperezp3/incident-hub). Los Items se gestionan como GitHub Issues; las claves mantienen la jerarquía para la revisión del proyecto. Responsable: Mario Pérez (@fernandoperezp3). Estimaciones en horas.

## Epics y Features

| Clave | Tipo | Título | Issue | Padre | Prioridad | Est. |
|---|---|---|---:|---|---:|---:|
| E1 | Epic | Gestión operativa de incidentes | [#3](https://github.com/fernandoperezp3/incident-hub/issues/3) | — | P1 | 20 h |
| F1 | Feature | Registro y consulta | [#4](https://github.com/fernandoperezp3/incident-hub/issues/4) | E1 | P1 | 6 h |
| F2 | Feature | Asignación, estados y bitácora | [#5](https://github.com/fernandoperezp3/incident-hub/issues/5) | E1 | P1 | 7 h |
| E2 | Epic | Entrega continua y lanzamiento | [#6](https://github.com/fernandoperezp3/incident-hub/issues/6) | — | P1 | 22 h |
| F3 | Feature | Tablero, calidad y seguridad | [#7](https://github.com/fernandoperezp3/incident-hub/issues/7) | E2 | P1 | 9 h |
| F4 | Feature | Versionado y release controlado | [#8](https://github.com/fernandoperezp3/incident-hub/issues/8) | E2 | P2 | 7 h |

## Historias de usuario

| Clave | Feature | Historia | Issue | Prioridad | Est. |
|---|---|---|---:|---:|---:|
| US1 | F1 | Registrar un incidente con sus datos básicos. | [#9](https://github.com/fernandoperezp3/incident-hub/issues/9) | P1 | 3 h |
| US2 | F1 | Consultar y filtrar incidentes. | [#10](https://github.com/fernandoperezp3/incident-hub/issues/10) | P1 | 3 h |
| US3 | F2 | Asignar un técnico a cada caso. | [#11](https://github.com/fernandoperezp3/incident-hub/issues/11) | P1 | 2 h |
| US4 | F2 | Cambiar el estado para reflejar el avance. | [#12](https://github.com/fernandoperezp3/incident-hub/issues/12) | P1 | 2 h |
| US5 | F2 | Registrar comentarios de seguimiento. | [#13](https://github.com/fernandoperezp3/incident-hub/issues/13) | P1 | 3 h |
| US6 | F3 | Ver indicadores de volumen y prioridad. | [#14](https://github.com/fernandoperezp3/incident-hub/issues/14) | P1 | 3 h |
| US7 | F3 | Ejecutar validaciones y análisis de dependencias en PRs. | [#15](https://github.com/fernandoperezp3/incident-hub/issues/15) | P1 | 3 h |
| US8 | F4 | Publicar versiones con guía de reversión. | [#16](https://github.com/fernandoperezp3/incident-hub/issues/16) | P2 | 3 h |

## Tareas

| Clave | Historia | Trabajo | Issue | Prioridad | Est. |
|---|---|---|---:|---:|---:|
| T01 | US1 | Definir esquema y validación de incidentes. | [#17](https://github.com/fernandoperezp3/incident-hub/issues/17) | P1 | 1 h |
| T02 | US1 | Crear formulario y endpoint de alta. | [#18](https://github.com/fernandoperezp3/incident-hub/issues/18) | P1 | 2 h |
| T03 | US2 | Listar y ordenar incidentes. | [#19](https://github.com/fernandoperezp3/incident-hub/issues/19) | P1 | 1 h |
| T04 | US2 | Implementar filtros y búsqueda. | [#20](https://github.com/fernandoperezp3/incident-hub/issues/20) | P1 | 2 h |
| T05 | US3 | Implementar asignación de técnico. | [#21](https://github.com/fernandoperezp3/incident-hub/issues/21) | P1 | 1 h |
| T06 | US3 | Mostrar responsable en el tablero. | [#22](https://github.com/fernandoperezp3/incident-hub/issues/22) | P1 | 1 h |
| T07 | US4 | Validar transiciones de estado. | [#23](https://github.com/fernandoperezp3/incident-hub/issues/23) | P1 | 1 h |
| T08 | US4 | Añadir controles de flujo al detalle. | [#24](https://github.com/fernandoperezp3/incident-hub/issues/24) | P1 | 1 h |
| T09 | US5 | Persistir comentarios y eventos. | [#25](https://github.com/fernandoperezp3/incident-hub/issues/25) | P1 | 2 h |
| T10 | US5 | Presentar bitácora ordenada. | [#26](https://github.com/fernandoperezp3/incident-hub/issues/26) | P1 | 1 h |
| T11 | US6 | Calcular métricas de operación. | [#27](https://github.com/fernandoperezp3/incident-hub/issues/27) | P1 | 1 h |
| T12 | US6 | Mostrar gráficos por categoría y técnico. | [#28](https://github.com/fernandoperezp3/incident-hub/issues/28) | P1 | 2 h |
| T13 | US7 | Crear workflow de validación de PR. | [#29](https://github.com/fernandoperezp3/incident-hub/issues/29) | P1 | 1 h |
| T14 | US7 | Añadir pruebas, análisis de dependencias y artefacto. | [#30](https://github.com/fernandoperezp3/incident-hub/issues/30) | P1 | 2 h |
| T15 | US8 | Documentar SemVer, ambientes y promoción. | [#31](https://github.com/fernandoperezp3/incident-hub/issues/31) | P2 | 2 h |
| T16 | US8 | Preparar checklist de publicación y reversión. | [#32](https://github.com/fernandoperezp3/incident-hub/issues/32) | P2 | 1 h |
| T17 | US7 | Registrar y evidenciar el runner self-hosted de GitHub Actions. | [#33](https://github.com/fernandoperezp3/incident-hub/issues/33) | P2 | 2 h |

## Relaciones y evidencia

E1 contiene F1 y F2; E2 contiene F3 y F4. US1–US2 pertenecen a F1, US3–US5 a F2, US6–US7 a F3 y US8 a F4. Las tareas se relacionan con la historia indicada en su fila.

El Issue [#1](https://github.com/fernandoperezp3/incident-hub/issues/1) registra el fallo inicial de aislamiento de datos en las pruebas. Su corrección se integró mediante [PR #2](https://github.com/fernandoperezp3/incident-hub/pull/2); el primer run rojo y el run verde de Actions están enlazados en ese PR. T17 queda abierto hasta que se registre el runner en la computadora y exista evidencia de una ejecución self-hosted.
