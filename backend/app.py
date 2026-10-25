"""Small, dependency-free REST API for IT Incident Hub."""

from __future__ import annotations

import json
import mimetypes
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterator
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("INCIDENT_DB", ROOT / "database" / "incidents.db"))
STATUSES = {"NUEVO", "ASIGNADO", "EN_PROCESO", "RESUELTO", "CERRADO"}
PRIORITIES = {"BAJA", "MEDIA", "ALTA", "CRITICA"}
MAX_BODY_BYTES = 1024 * 1024


class PayloadTooLarge(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
    finally:
        conn.close()


def initialize() -> None:
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS incidents (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          description TEXT NOT NULL,
          category TEXT NOT NULL,
          priority TEXT NOT NULL CHECK(priority IN ('BAJA','MEDIA','ALTA','CRITICA')),
          reporter TEXT NOT NULL,
          technician TEXT,
          status TEXT NOT NULL DEFAULT 'NUEVO' CHECK(status IN ('NUEVO','ASIGNADO','EN_PROCESO','RESUELTO','CERRADO')),
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS activity (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
          author TEXT NOT NULL,
          message TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status);
        CREATE INDEX IF NOT EXISTS idx_incidents_priority ON incidents(priority);
        """)
        if db.execute("SELECT COUNT(*) FROM incidents").fetchone()[0] == 0:
            stamp = now()
            examples = [
                ("No puedo acceder al correo", "Outlook solicita credenciales repetidamente desde esta mañana.", "Acceso", "ALTA", "Ana López", "Carlos Méndez", "EN_PROCESO"),
                ("Impresora de recepción sin conexión", "La impresora de red aparece fuera de línea.", "Hardware", "MEDIA", "Luis Pérez", None, "NUEVO"),
                ("Solicitud de acceso a VPN", "Necesito acceso remoto para trabajar esta semana.", "Red", "BAJA", "María García", "Sofía Ruiz", "ASIGNADO"),
                ("Sistema de ventas no disponible", "El sistema muestra error 503 para todo el equipo.", "Aplicaciones", "CRITICA", "Diego Morales", "Carlos Méndez", "RESUELTO"),
            ]
            db.executemany("INSERT INTO incidents(title,description,category,priority,reporter,technician,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)", [(*x, stamp, stamp) for x in examples])
            first_incident_id = db.execute("SELECT id FROM incidents WHERE title=?", (examples[0][0],)).fetchone()[0]
            db.execute("INSERT INTO activity(incident_id,author,message,created_at) VALUES(?,'Carlos Méndez','Se está revisando la configuración de la cuenta.',?)", (first_incident_id, stamp))


def incident_dict(row: sqlite3.Row, db: sqlite3.Connection) -> dict:
    item = dict(row)
    item["activity"] = [dict(a) for a in db.execute("SELECT id, author, message, created_at FROM activity WHERE incident_id=? ORDER BY id", (item["id"],))]
    return item


class Handler(BaseHTTPRequestHandler):
    server_version = "IncidentHub/1.0"

    def send_json(self, status: int, payload: object) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(data)

    def body(self) -> dict:
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            raise ValueError("Content-Length no es válido.")
        if size < 0:
            raise ValueError("Content-Length no es válido.")
        if size > MAX_BODY_BYTES:
            raise PayloadTooLarge("El cuerpo supera el límite de 1 MiB.")
        try:
            payload = json.loads(self.rfile.read(size) or b"{}")
        except json.JSONDecodeError:
            raise ValueError("El cuerpo debe ser JSON válido.")
        if not isinstance(payload, dict):
            raise ValueError("El cuerpo JSON debe ser un objeto.")
        return payload

    def do_OPTIONS(self) -> None:
        self.send_json(200, {"ok": True})

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path.startswith("/styles.css") or parsed.path.startswith("/app.js"):
            name = "index.html" if parsed.path == "/" else parsed.path.lstrip("/")
            target = (ROOT / "frontend" / name).resolve()
            if target.parent == (ROOT / "frontend").resolve() and target.is_file():
                data = target.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        with connect() as db:
            if parsed.path == "/api/health":
                return self.send_json(200, {"status": "ok"})
            if parsed.path == "/api/metrics":
                total = db.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
                open_count = db.execute("SELECT COUNT(*) FROM incidents WHERE status NOT IN ('RESUELTO','CERRADO')").fetchone()[0]
                closed = db.execute("SELECT COUNT(*) FROM incidents WHERE status='CERRADO'").fetchone()[0]
                critical = db.execute("SELECT COUNT(*) FROM incidents WHERE priority='CRITICA' AND status NOT IN ('RESUELTO','CERRADO')").fetchone()[0]
                categories = [dict(row) for row in db.execute("SELECT category,COUNT(*) AS count FROM incidents GROUP BY category ORDER BY count DESC, category")]
                technicians = [dict(row) for row in db.execute("SELECT COALESCE(technician,'Sin asignar') AS technician,COUNT(*) AS count FROM incidents GROUP BY technician ORDER BY count DESC")]
                return self.send_json(200, {"total": total, "open": open_count, "closed": closed, "critical": critical, "by_category": categories, "by_technician": technicians})
            if parsed.path == "/api/incidents":
                clauses, values = [], []
                for key in ("status", "priority", "category", "technician"):
                    if query.get(key):
                        clauses.append("technician IS NULL" if key == "technician" and query[key] == "Sin asignar" else f"{key} = ?")
                        if not (key == "technician" and query[key] == "Sin asignar"):
                            values.append(query[key])
                try:
                    limit = int(query.get("limit", "100"))
                    offset = int(query.get("offset", "0"))
                except ValueError:
                    return self.send_json(400, {"error": "Límite y desplazamiento deben ser números enteros."})
                if limit < 1 or limit > 100 or offset < 0:
                    return self.send_json(400, {"error": "El límite debe estar entre 1 y 100 y el desplazamiento no puede ser negativo."})
                where = " WHERE " + " AND ".join(clauses) if clauses else ""
                order = " ORDER BY CASE priority WHEN 'CRITICA' THEN 0 WHEN 'ALTA' THEN 1 WHEN 'MEDIA' THEN 2 ELSE 3 END, id DESC"
                total = db.execute("SELECT COUNT(*) FROM incidents" + where, values).fetchone()[0]
                sql = "SELECT * FROM incidents" + where + order + " LIMIT ? OFFSET ?"
                items = [incident_dict(row, db) for row in db.execute(sql, values + [limit, offset])]
                next_offset = offset + len(items) if offset + len(items) < total else None
                return self.send_json(200, {"items": items, "pagination": {"total": total, "limit": limit, "offset": offset, "next_offset": next_offset}})
            parts = parsed.path.strip("/").split("/")
            if len(parts) == 3 and parts[:2] == ["api", "incidents"] and parts[2].isdigit():
                row = db.execute("SELECT * FROM incidents WHERE id=?", (int(parts[2]),)).fetchone()
                return self.send_json(200, incident_dict(row, db)) if row else self.send_json(404, {"error": "Incidente no encontrado."})
        self.send_json(404, {"error": "Ruta no encontrada."})

    def do_POST(self) -> None:
        try:
            payload = self.body()
            parts = urlparse(self.path).path.strip("/").split("/")
            with connect() as db:
                if parts == ["api", "incidents"]:
                    required = ("title", "description", "category", "priority", "reporter")
                    if any(not str(payload.get(k, "")).strip() for k in required):
                        return self.send_json(400, {"error": "Completa título, descripción, categoría, prioridad y usuario."})
                    if payload["priority"] not in PRIORITIES:
                        return self.send_json(400, {"error": "Prioridad no válida."})
                    stamp = now()
                    cur = db.execute("INSERT INTO incidents(title,description,category,priority,reporter,created_at,updated_at) VALUES(?,?,?,?,?,?,?)", tuple(str(payload[k]).strip() for k in required) + (stamp, stamp))
                    db.execute("INSERT INTO activity(incident_id,author,message,created_at) VALUES(?,?,?,?)", (cur.lastrowid, payload["reporter"], "Incidente creado.", stamp))
                    return self.send_json(201, incident_dict(db.execute("SELECT * FROM incidents WHERE id=?", (cur.lastrowid,)).fetchone(), db))
                if len(parts) == 4 and parts[:2] == ["api", "incidents"] and parts[2].isdigit() and parts[3] == "activity":
                    incident_id = int(parts[2])
                    if not db.execute("SELECT 1 FROM incidents WHERE id=?", (incident_id,)).fetchone():
                        return self.send_json(404, {"error": "Incidente no encontrado."})
                    author, message = str(payload.get("author", "")).strip(), str(payload.get("message", "")).strip()
                    if not author or not message:
                        return self.send_json(400, {"error": "Autor y comentario son obligatorios."})
                    db.execute("INSERT INTO activity(incident_id,author,message,created_at) VALUES(?,?,?,?)", (incident_id, author, message, now()))
                    return self.send_json(201, {"ok": True})
            self.send_json(404, {"error": "Ruta no encontrada."})
        except PayloadTooLarge as exc:
            self.close_connection = True
            self.send_json(413, {"error": str(exc)})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})

    def do_PATCH(self) -> None:
        try:
            payload = self.body()
            parts = urlparse(self.path).path.strip("/").split("/")
            if len(parts) != 3 or parts[:2] != ["api", "incidents"] or not parts[2].isdigit():
                return self.send_json(404, {"error": "Ruta no encontrada."})
            incident_id = int(parts[2])
            with connect() as db:
                row = db.execute("SELECT * FROM incidents WHERE id=?", (incident_id,)).fetchone()
                if not row:
                    return self.send_json(404, {"error": "Incidente no encontrado."})
                changes, activity = [], []
                if "status" in payload:
                    if payload["status"] not in STATUSES:
                        return self.send_json(400, {"error": "Estado no válido."})
                    if payload["status"] != row["status"]:
                        changes.append(("status", payload["status"]))
                        activity.append(f"Estado cambiado de {row['status']} a {payload['status']}.")
                if "technician" in payload:
                    technician = str(payload["technician"]).strip() or None
                    if technician != row["technician"]:
                        changes.append(("technician", technician))
                        activity.append(f"Técnico asignado: {technician or 'Sin asignar'}.")
                        if technician and row["status"] == "NUEVO" and "status" not in payload:
                            changes.append(("status", "ASIGNADO"))
                            activity.append("Estado cambiado de NUEVO a ASIGNADO.")
                if not changes:
                    return self.send_json(400, {"error": "Indica un estado o técnico diferente."})
                assignments = ",".join(f"{key}=?" for key, _ in changes)
                db.execute(f"UPDATE incidents SET {assignments}, updated_at=? WHERE id=?", [v for _, v in changes] + [now(), incident_id])
                db.executemany("INSERT INTO activity(incident_id,author,message,created_at) VALUES(?,?,?,?)", [(incident_id, "Sistema", note, now()) for note in activity])
                return self.send_json(200, incident_dict(db.execute("SELECT * FROM incidents WHERE id=?", (incident_id,)).fetchone(), db))
        except PayloadTooLarge as exc:
            self.close_connection = True
            self.send_json(413, {"error": str(exc)})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")


def serve() -> None:
    initialize()
    port = int(os.environ.get("PORT", "8000"))
    print(f"IT Incident Hub API: http://localhost:{port}/api/health")
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    serve()

