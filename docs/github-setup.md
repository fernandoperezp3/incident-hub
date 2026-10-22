# Configuración de GitHub y runner autohospedado

## Repositorio único

Crear un repositorio privado llamado `incident-hub` en la cuenta del estudiante. Subir el contenido del workspace y conservar una sola rama principal llamada `main`. No subir la base de datos local, tokens, claves ni archivos `.env`. Después de conectar el repo, añadir su URL a este documento y al README.

## Ajustes del repositorio

1. Activar GitHub Issues y crear los ítems de `docs/backlog.md`; añadirlos a un GitHub Project con los campos sugeridos.
2. En Settings → Rules/Branches, proteger `main`: exigir Pull Request y que pase `CI / Validate, test and package`. En una cuenta individual, acordar con el instructor cómo evidenciar revisión sin autoaprobar.
3. Habilitar dependency graph y, si la cuenta lo permite, Dependabot alerts y security updates.
4. Configurar GitHub Environment `demo` para una publicación futura. Guardar valores sensibles solo como Environment secrets; no crear secrets ficticios si no hay despliegue.
5. Activar Releases y publicar tags SemVer después del checklist de `docs/release.md`.

## Runner autohospedado Windows

La consigna solicita un agente autohospedado de Azure. Como no hay cuenta Azure, la adaptación equivalente es un **self-hosted runner de GitHub Actions** en una computadora propia.

1. En el repo: Settings → Actions → Runners → New self-hosted runner → Windows x64. Seguir los comandos que GitHub presenta para ese repositorio; el token de registro es temporal y no debe guardarse en documentación ni commits.
2. Instalar el runner en una carpeta dedicada, aceptar únicamente el uso previsto para este repo y probarlo sin ejecutar código de repositorios ajenos.
3. Para uso permanente, instalarlo como servicio desde la carpeta del runner y comprobar que aparezca `Idle` en Settings → Actions → Runners.
4. Añadir una etiqueta propia, por ejemplo `incident-hub`, y crear un workflow manual separado que use `runs-on: [self-hosted, incident-hub]`. Ejecutarlo con un cambio inocuo y guardar URL del workflow y log exitoso como evidencia.
5. Deshabilitar o desinstalar el runner al terminar la demostración si el equipo no necesita más ejecuciones.

No se ha conectado ni usado un runner desde este workspace; primero debe existir el repositorio en GitHub y completarse el alta siguiendo los comandos emitidos por la propia cuenta.

## Demostración de fallo controlado

En una rama de práctica, introducir un cambio deliberado y reversible que haga fallar una validación, abrir PR, capturar el enlace del run, registrar el diagnóstico en el Issue, corregirlo en otro commit y guardar el run verde. No poner credenciales en el cambio. La falla controlada todavía está pendiente.
