import os

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename, send_from_directory

from middleware.auth import require_api_key

MARKDOWN_DIR = os.environ.get("MARKDOWN_DIR", "./data/uploads")
os.makedirs(MARKDOWN_DIR, exist_ok=True)

content_bp = Blueprint('api/content', __name__)

@content_bp.get('/')
def list_content():
    """Listet alle Markdown-Dateien im Storage-Verzeichnis auf."""

    try:
        files = [
            f for f in os.listdir(MARKDOWN_DIR)
            if os.path.isfile(os.path.join(MARKDOWN_DIR, f)) and f.lower().endswith('.md')
        ]

        return jsonify({"files": files}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@content_bp.get('/content/<string:filename>')
def content(filename):
    """Gibt eine Markdown-Datei zurück."""

    filename = secure_filename(filename)

    path = os.path.join(MARKDOWN_DIR, filename)

    if not os.path.exists(path):
        return jsonify({"error": "Datei nicht gefunden"}), 404

    return send_from_directory(MARKDOWN_DIR, filename, mimetype="text/markdown")


@content_bp.post('/upload')
@require_api_key
def upload():
    """Speichert eine Markdown-Datei im Storage-Verzeichnis."""

    if 'file' not in request.files:
        return jsonify({"error": "Feld 'file' fehlt."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Keine Datei ausgewählt."}), 400

    if not file.filename.lower().endswith('.md'):
        return jsonify({"error": "Nur .md Dateien erlaubt."}), 400

    try:
        filename = secure_filename(file.filename)
        path = os.path.join(MARKDOWN_DIR, filename)

        file.save(path)

        return jsonify({
            "status": "success",
            "filename": filename
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500