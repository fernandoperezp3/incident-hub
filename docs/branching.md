# Branching, revisión y evidencia

- `main` debe contener únicamente cambios integrados y con CI correcta.
- Crear una rama por Issue: `feature/<n>-<resumen>`, `fix/<n>-<resumen>` o `refactor/<n>-<resumen>`.
- Hacer commits pequeños y descriptivos con la referencia `#N` del Issue.
- Abrir PR contra `main`, completar el template, pedir revisión y registrar evidencia de validación.
- Activar en GitHub la protección de `main`: PR requerido, al menos una aprobación si la configuración individual lo permite y estado de CI obligatorio. No autoaprobar los propios cambios; solicitar la revisión disponible según las reglas de la clase.
- Integrar mediante squash o merge commit después de aprobar; borrar ramas ya integradas.

## Flujo de integración y evidencia en GitHub

El repositorio tiene cambios reales integrados mediante pull requests: [#2](https://github.com/fernandoperezp3/incident-hub/pull/2), [#34](https://github.com/fernandoperezp3/incident-hub/pull/34), [#37](https://github.com/fernandoperezp3/incident-hub/pull/37), [#38](https://github.com/fernandoperezp3/incident-hub/pull/38), [#39](https://github.com/fernandoperezp3/incident-hub/pull/39) y [#41–#48](https://github.com/fernandoperezp3/incident-hub/pulls?q=is%3Apr+is%3Amerged).

El workflow `.github/workflows/ci.yml` ejecuta validaciones, pruebas, auditoría de dependencias y empaquetado. El [PR #2](https://github.com/fernandoperezp3/incident-hub/pull/2) conserva la corrección del fallo inicial de pruebas y sus ejecuciones de CI. El [PR #47](https://github.com/fernandoperezp3/incident-hub/pull/47) corrigió el formulario de incidentes y fue aprobado antes de fusionarse. El runner Windows se verificó en [esta ejecución](https://github.com/fernandoperezp3/incident-hub/actions/runs/39878187941).

El [PR #48](https://github.com/fernandoperezp3/incident-hub/pull/48) añadió el informe final de pruebas al repositorio; su validación de CI terminó correctamente en [run 40236405780](https://github.com/fernandoperezp3/incident-hub/actions/runs/40236405780).
