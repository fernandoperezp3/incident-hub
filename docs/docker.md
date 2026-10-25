# Ejecución con Docker

Docker Desktop debe estar abierto y mostrar que el motor está activo.

## Aplicación

Desde la raíz del repositorio, ejecutar:

```powershell
docker compose up --build -d
docker compose ps
```

Abrir <http://localhost:8000>. El servicio publica el puerto solo en la computadora local y conserva la base SQLite en el volumen `incidents-data`.

## Pruebas automatizadas

```powershell
docker compose --profile test run --rm tests
```

## Detener la aplicación

```powershell
docker compose down
```

La base de datos del volumen permanece disponible para la siguiente ejecución.
