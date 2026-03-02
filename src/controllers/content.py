from flask import Blueprint, request, jsonify
from sqlalchemy import select

from src.db import db
from src.middleware.auth import require_api_key
from src.models.content import ContentEntity

content_bp = Blueprint('api/content', __name__)

@content_bp.get('/')
def index():
    """Listet alle Content-IDs und Dateinamen auf."""
    entries = db.session.execute(select(ContentEntity)).scalars().all()

    return jsonify([
        {"id": str(entry.id), "filename": entry.filename}
        for entry in entries
    ]), 200

@content_bp.get('/content/<int:id>')
def content(id):
    """Gibt den Content einer bestimmten Datei zurück."""
    entry = db.session.execute(
        select(ContentEntity).where(ContentEntity.id == id)
    ).scalars().first()

    return jsonify(
        {
            "id": str(entry.id),
            "filename": entry.filename,
            "content": entry.markdown_content
        }
    ), 200


@content_bp.post('/upload')
@require_api_key
def upload():
    """Speichert den Inhalt einer Markdown-Datei in der Spalte 'markdown_content'."""
    if 'file' not in request.files:
        return jsonify({"error": "Feld 'file' fehlt."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Keine Datei ausgewählt."}), 400

    if not file.filename.lower().endswith('.md'):
        return jsonify({"error": "Nur .md Dateien erlaubt."}), 400

    try:
        # Inhalt auslesen
        content_str = file.read().decode('utf-8')

        new_content = ContentEntity(
            filename=file.filename,
            markdown_content=content_str
        )

        db.session.add(new_content)
        db.session.commit()

        return jsonify({
            "status": "success",
            "id": str(new_content.id),
            "filename": new_content.filename
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500