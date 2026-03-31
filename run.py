"""
Development server entry point.

    python run.py
"""
import os
from src import create_app

app = create_app()

if __name__ == "__main__":
    cert = os.path.join("certs", "localhost.pem")
    key  = os.path.join("certs", "localhost-key.pem")
    ssl_ctx = (cert, key) if os.path.exists(cert) else None
    scheme = "https" if ssl_ctx else "http"
    print(f" * Running on {scheme}://localhost:5001")
    app.run(debug=True, port=5001, ssl_context=ssl_ctx)
