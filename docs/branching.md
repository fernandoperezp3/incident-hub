# Branching, revisión y evidencia

- `main` debe contener únicamente cambios integrados y con CI correcta.
- Crear una rama por Issue: `feature/<n>-<resumen>`, `fix/<n>-<resumen>` o `refactor/<n>-<resumen>`.
- Hacer commits pequeños y descriptivos con la referencia `#N` del Issue.
- Abrir PR contra `main`, completar el template, pedir revisión y registrar evidencia de validación.
- Activar en GitHub la protección de `main`: PR requerido, al menos una aprobación si la configuración individual lo permite y estado de CI obligatorio. No autoaprobar los propios cambios; solicitar la revisión disponible según las reglas de la clase.
- Integrar mediante squash o merge commit después de aprobar; borrar ramas ya integradas.

## Evidencia que aún debe producirse en GitHub

El código local no constituye evidencia de PR revisadas ni de runs reales. Planificar al menos seis PR pequeñas y reales durante el trabajo, y conservar sus URLs, revisiones y runs: 1) esqueleto/API, 2) alta/listado, 3) asignación/bitácora, 4) métricas, 5) hardening y pruebas, 6) release. No crear PR ficticias ni afirmar aprobación sin que ocurra.

El workflow en `.github/workflows/ci.yml` hace validación, pruebas, auditoría y artefacto. Para evidenciar un fallo controlado, introducir de manera deliberada un fallo en una rama descartable o PR de práctica, guardar el run y corregirlo en el flujo normal; documentar diagnóstico y run exitoso. Nunca publicar secretos para provocar fallos.
