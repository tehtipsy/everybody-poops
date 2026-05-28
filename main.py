import csv
import json
from datetime import datetime
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from urllib.parse import parse_qs, urlparse

from dal import logs, new_unique_id
from dummy_data import get_dummy_logs


def _render_page(message=""):
    rows = []
    for entry in logs:
        rows.append(
            f"""
            <tr>
                <td>{escape(str(entry["id"]))}</td>
                <td>{escape(str(entry["type"]))}</td>
                <td>{escape(str(entry["notes"]))}</td>
                <td>{escape(str(entry["timestamp"]))}</td>
                <td>
                    <form method="post" action="/edit" style="display:inline-block">
                        <input type="hidden" name="id" value="{escape(str(entry["id"]))}">
                        <select name="type">
                            <option value="1">1</option>
                            <option value="2">2</option>
                        </select>
                        <input type="text" name="notes" placeholder="new notes">
                        <button type="submit">Update</button>
                    </form>
                </td>
            </tr>
            """
        )

    message_html = f"<p>{escape(message)}</p>" if message else ""
    return f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>Everybody Poops</title></head>
<body>
    <h1>Everybody Poops</h1>
    {message_html}
    <h2>Log an Entry</h2>
    <form method="post" action="/log">
        <label>Type:</label>
        <select name="type">
            <option value="1">1</option>
            <option value="2">2</option>
        </select>
        <label>Notes:</label>
        <input type="text" name="notes">
        <button type="submit">Log</button>
    </form>
    <h2>Actions</h2>
    <form method="post" action="/load-dummy">
        <button type="submit">Load Dummy Data</button>
    </form>
    <p><a href="/history">View JSON history</a></p>
    <p><a href="/export.json">Export JSON</a></p>
    <p><a href="/export.csv">Export CSV</a></p>
    <h2>History</h2>
    <table border="1" cellpadding="4" cellspacing="0">
        <tr><th>ID</th><th>Type</th><th>Notes</th><th>Timestamp</th><th>Edit</th></tr>
        {''.join(rows)}
    </table>
</body>
</html>
"""


class EverybodyPoopsHandler(BaseHTTPRequestHandler):
    def _read_form(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length).decode("utf-8")
        return parse_qs(raw)

    def _send_html(self, html, status=200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload, filename=None):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_csv(self):
        output = StringIO()
        fieldnames = ["id", "type", "notes", "timestamp"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for entry in logs:
            writer.writerow({key: entry.get(key, "") for key in fieldnames})
        body = output.getvalue().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", 'attachment; filename="everybody-poops.csv"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect_home(self):
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send_html(_render_page())
            return
        if path == "/history":
            self._send_json(logs)
            return
        if path == "/export.json":
            self._send_json(logs, filename="everybody-poops.json")
            return
        if path == "/export.csv":
            self._send_csv()
            return
        self._send_html("<h1>Not Found</h1>", status=404)

    def do_POST(self):
        path = urlparse(self.path).path
        form = self._read_form()

        if path == "/log":
            type_value = form.get("type", [""])[0]
            if type_value not in {"1", "2"}:
                self._send_html(_render_page("Invalid type. Use 1 or 2."), status=400)
                return
            logs.append(
                {
                    "id": new_unique_id(),
                    "type": type_value,
                    "notes": form.get("notes", [""])[0],
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                }
            )
            self._redirect_home()
            return

        if path == "/edit":
            target_id = form.get("id", [""])[0].strip()
            new_type = form.get("type", [""])[0]
            new_notes = form.get("notes", [""])[0]
            for entry in logs:
                if str(entry.get("id", "")).upper() == target_id.upper():
                    if new_type in {"1", "2"}:
                        entry["type"] = new_type
                    if new_notes:
                        entry["notes"] = new_notes
                    break
            self._redirect_home()
            return

        if path == "/load-dummy":
            logs.clear()
            logs.extend(get_dummy_logs())
            self._redirect_home()
            return

        self._send_html("<h1>Not Found</h1>", status=404)


def create_server(host="0.0.0.0", port=8000):
    return ThreadingHTTPServer((host, port), EverybodyPoopsHandler)


def main():
    server = create_server()
    print("Serving Everybody Poops web app on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    main()