# Versionado y lanzamiento

## SemVer

Usar `MAJOR.MINOR.PATCH`: cambio incompatible → MAJOR; funcionalidad compatible → MINOR; corrección compatible → PATCH. La primera entrega está publicada como `v1.0.0` en [GitHub Releases](https://github.com/fernandoperezp3/incident-hub/releases/tag/v1.0.0), sobre el commit integrado en `main`.

## Ambientes y promoción

1. **Local:** iniciar con `python backend/app.py` y usar datos sintéticos.
2. **CI de GitHub:** compila Python, ejecuta pruebas de API, analiza dependencias con `pip-audit` y publica un ZIP identificado por SHA.
3. **Runner propio:** el runner Windows está registrado con etiqueta `incident-hub`; su workflow terminó correctamente en [run 39878187941](https://github.com/fernandoperezp3/incident-hub/actions/runs/39878187941). No se usa Azure.
4. **Release:** CI y runner se validaron antes de publicar la release [v1.0.0](https://github.com/fernandoperezp3/incident-hub/releases/tag/v1.0.0). Incluye el ZIP producido por el CI del commit `3ae43c20e5cf1eb40636001c55b5eabb4b19f650`.

## Evidencia disponible

| Cambio | Pull Request | Validación |
|---|---|---|
| Aislamiento de pruebas y empaquetado | [#2](https://github.com/fernandoperezp3/incident-hub/pull/2) | [run 39817414741](https://github.com/fernandoperezp3/incident-hub/actions/runs/39817414741) |
| Backlog y guía GitHub | [#34](https://github.com/fernandoperezp3/incident-hub/pull/34) | [run 39819267718](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819267718) |
| Paginación API | [#37](https://github.com/fernandoperezp3/incident-hub/pull/37) | [run 39819695858](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819695858) |
| Límite de cuerpo JSON | [#38](https://github.com/fernandoperezp3/incident-hub/pull/38) | [run 39819966156](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819966156) |
| Preparación del runner Windows | [#39](https://github.com/fernandoperezp3/incident-hub/pull/39) | [run 39820089542](https://github.com/fernandoperezp3/incident-hub/actions/runs/39820089542) |
| Corrección del workflow para Windows | [#42](https://github.com/fernandoperezp3/incident-hub/pull/42) y [#43](https://github.com/fernandoperezp3/incident-hub/pull/43) | [CI verde](https://github.com/fernandoperezp3/incident-hub/actions/runs/39878187858) y [runner Windows verde](https://github.com/fernandoperezp3/incident-hub/actions/runs/39878187941) |

## Checklist de salida

- [x] Cerrar los Issues incluidos en la entrega y conservar la trazabilidad con PRs.
- [x] CI verde en el commit de `main` publicado.
- [x] Ejecutar el workflow self-hosted y conservar la URL del run.
- [x] Documentar el inventario de dependencias y la deuda técnica.
- [ ] Iniciar la aplicación local con datos ficticios y revisar el flujo principal durante la demostración final.
- [x] Crear tag `v1.0.0`, publicar Release notes y adjuntar el ZIP del commit etiquetado.
- [x] Registrar la URL del Release y la evidencia de validación.

## Reversión

Para la demo local, conservar una copia de la base de datos antes de sustituir el ZIP. Volver al tag anterior si la revisión manual falla. No sobrescribir datos reales. Para un futuro ambiente hospedado, definir y ensayar restauración de la base, health check y promoción de la versión previa antes de habilitar tráfico.

La release `v1.0.0` está publicada. El proyecto se entrega en un solo repositorio GitHub y no depende de Azure; la demostración final se hace localmente con datos ficticios.
