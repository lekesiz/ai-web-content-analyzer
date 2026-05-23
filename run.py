"""Application entry point.

Exposes ``app`` for WSGI servers (gunicorn) and runs the dev server
when executed directly.
"""
from app import create_app, db

app = create_app()

# Create tables idempotently on boot. Wrapping in try/except protects
# against transient DB unavailability at worker boot (gunicorn forks
# multiple workers in parallel which can race on schema creation).
with app.app_context():
    try:
        db.create_all()
    except Exception as exc:  # pragma: no cover - boot-time defensive guard
        import sys
        print(f"[run.py] Warning: db.create_all() failed at boot: {exc}", file=sys.stderr)
        # Do not raise; the request handler will surface a clearer
        # error if the DB is genuinely misconfigured.

if __name__ == '__main__':
    app.run(debug=True, port=5000)
