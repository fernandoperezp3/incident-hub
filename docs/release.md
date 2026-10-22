# Versionado y lanzamiento

## SemVer

Usar `MAJOR.MINOR.PATCH`: cambio incompatible → MAJOR; funcionalidad compatible → MINOR; corrección compatible → PATCH. La primera entrega académica se publicará como `v1.0.0` cuando estén completos los criterios de salida. No existe todavía un tag ni un GitHub Release publicado.

## Ambientes y promoción

1. **Local:** iniciar con `python backend/app.py` y usar datos sintéticos.
2. **CI de GitHub:** compila Python, ejecuta comprobaciones de API, analiza el inventario con `pip-audit` y publica un ZIP inmutable identificado por SHA.
3. **Runner propio:** ejecutar el workflow manual de Windows después de registrar el runner con etiqueta `incident-hub`. No se usa Azure.
4. **Release:** después de validar CI y el runner, etiquetar el commit integrado de `main` como `v1.0.0`, crear GitHub Release y adjuntar el artefacto de ese commit.

## Evidencia disponible

| Cambio | Pull Request | Validación |
|---|---|---|
| Aislamiento de pruebas y empaquetado | [#2](https://github.com/fernandoperezp3/incident-hub/pull/2) | [run 39817414741](https://github.com/fernandoperezp3/incident-hub/actions/runs/39817414741) |
| Backlog y guía GitHub | [#34](https://github.com/fernandoperezp3/incident-hub/pull/34) | [run 39819267718](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819267718) |
| Paginación API | [#37](https://github.com/fernandoperezp3/incident-hub/pull/37) | [run 39819695858](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819695858) |
| Límite de cuerpo JSON | [#38](https://github.com/fernandoperezp3/incident-hub/pull/38) | [run 39819966156](https://github.com/fernandoperezp3/incident-hub/actions/runs/39819966156) |
| Preparación del runner Windows | [#39](https://github.com/fernandoperezp3/incident-hub/pull/39) | [run 39820089542](https://github.com/fernandoperezp3/incident-hub/actions/runs/39820089542) valida el workflow principal; el runner Windows aún no se ha ejecutado. |

## Checklist de salida

- [ ] Cerrar los Issues incluidos en la entrega y vincularlos con PRs.
- [ ] CI verde en el commit de `main` que se va a publicar.
- [ ] Ejecutar el workflow self-hosted y conservar la URL del run.
- [ ] Confirmar el inventario de dependencias y el registro de deuda.
- [ ] Iniciar la aplicación local con datos ficticios y revisar el flujo principal.
- [ ] Crear tag `v1.0.0`, Release notes y adjuntar el ZIP del commit etiquetado.
- [ ] Registrar la URL del Release y evidencia de validación.

## Reversión

Para la demo local, conservar una copia de la base de datos antes de sustituir el ZIP. Volver al tag anterior si la revisión manual falla. No sobrescribir datos reales. Para un futuro ambiente hospedado, definir y ensayar restauración de la base, health check y promoción de la versión previa antes de habilitar tráfico.

La publicación final queda pendiente hasta que el runner self-hosted quede registrado y produzca una ejecución exitosa en la computadora propia. El seguimiento está en [Issue #33](https://github.com/fernandoperezp3/incident-hub/issues/33).
