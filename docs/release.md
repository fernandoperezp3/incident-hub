# Versionado y lanzamiento

## SemVer

Usar `MAJOR.MINOR.PATCH`: incompatible → MAJOR; funcionalidad compatible → MINOR; corrección compatible → PATCH. La secuencia prevista es `0.1.0` prototipo, `0.2.0` funcionalidad estabilizada, `0.3.0` hardening y evidencia DevOps, `1.0.0` primera entrega académica. Ajustar la secuencia a cambios efectivamente integrados y crear Tags/Releases reales en GitHub.

## Ambientes y promoción

1. **Local:** ejecutar y probar con datos sintéticos.
2. **CI:** GitHub Actions valida PR y produce ZIP inmutable por SHA.
3. **Demo/Release:** elegir un artefacto de un commit integrado, verificar pruebas y checklist, crear tag SemVer y GitHub Release. Un ambiente de hosting real queda fuera del alcance hasta elegir proveedor y cuenta.

## Checklist de salida

- [ ] Todos los Issues de la versión están cerrados y vinculados.
- [ ] PR revisadas; CI verde y artefacto asociado al commit.
- [ ] Dependencias y deuda técnica documentadas; sin secretos.
- [ ] Smoke check en el ambiente de demo con datos ficticios.
- [ ] Crear tag `vX.Y.Z`, notas de cambios, artefacto y pasos de reversión.
- [ ] Registrar URL de Release y evidencia de validación.

## Reversión

Para la demo local, conservar copia de la base de datos antes de sustituir el ZIP; volver a la versión etiquetada previa si el smoke check falla. No sobrescribir datos reales. Si luego se crea un ambiente hospedado, definir y ensayar restauración de base de datos, health check y promoción de la versión anterior antes de habilitar tráfico.
