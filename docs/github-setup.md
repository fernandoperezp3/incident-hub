# Configuración de GitHub y runner autohospedado

## Repositorio único

El proyecto está en el repositorio público [fernandoperezp3/incident-hub](https://github.com/fernandoperezp3/incident-hub), con `main` como rama principal. El alcance vigente usa GitHub Issues y GitHub Actions. La instrucción inicial sobre tres repositorios y Azure fue reemplazada por la confirmación del ingeniero: un solo repositorio y sin cuenta Azure.

No subir la base local, tokens, claves ni archivos `.env`.

## Ajustes recomendados del repositorio

1. Los ítems del backlog se encuentran como Issues enlazados en [docs/backlog.md](backlog.md).
2. Proteger `main` con Pull Requests y CI verde si las opciones del plan de GitHub lo permiten. Para el proyecto individual, el historial de PRs y la revisión técnica quedan como evidencia.
3. El workflow ejecuta `pip-audit`; el runtime base no declara dependencias externas. No añadir Dependency Review Action mientras Dependency Graph no esté habilitado.
4. No configurar un Environment o secretos ficticios mientras no exista un despliegue.
5. Publicar tags SemVer y Releases después de completar [docs/release.md](release.md).

## Runner self-hosted Windows

La alternativa al agente Azure es un **self-hosted runner de GitHub Actions** en una computadora propia.

1. En el repositorio, abrir Settings → Actions → Runners → New self-hosted runner → Windows x64.
2. Seguir solo las instrucciones y comandos temporales que emite GitHub para este repositorio. El token de registro no se comparte ni se guarda en documentación o commits.
3. Instalarlo en una carpeta dedicada, aceptar únicamente el uso previsto para este repositorio y evitar ejecutar código de repositorios ajenos.
4. Para uso permanente, instalar el runner como servicio y comprobar que figure como `Idle`.
5. Añadir la etiqueta `incident-hub`. El workflow manual [self-hosted.yml](../.github/workflows/self-hosted.yml) usa las etiquetas `self-hosted`, `Windows`, `X64` e `incident-hub`; solo muestra la versión de Python, Git y el nombre del runner, sin descargar ni ejecutar código del repositorio.
6. Después de registrar el runner, abrir Actions → Self-hosted runner demo → Run workflow, ejecutar la verificación y guardar el enlace del run como evidencia.
7. Deshabilitar o desinstalar el runner después de la demostración si ya no se necesita.

La inscripción y la evidencia de una ejecución self-hosted siguen pendientes; se registran en [Issue #33](https://github.com/fernandoperezp3/incident-hub/issues/33). Esta parte requiere que la computadora permanezca disponible para ejecutar el servicio.

## Demostración de fallo controlado

PR #2 conserva evidencia de una validación que falló al inicio por estado compartido de las pruebas y de una ejecución posterior verde tras corregir el aislamiento, las IDs de SQLite y la ruta del artefacto.
