"""
Pawan Studio AI — Flask PWA host
Run locally: python app.py
Production: gunicorn app:app
"""
import os
from flask import Flask, Response, jsonify, send_from_directory, make_response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)

# This app does not accept or store user images. CORS is enabled for the
# public, read-only PWA routes. Restrict origins if you later add private APIs.
@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, HEAD, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    # Avoid caching HTML aggressively so deployments update promptly.
    if response.mimetype == "text/html":
        response.headers["Cache-Control"] = "no-cache"
    return response

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/health")
def health():
    return jsonify(status="ok", service="Pawan Studio AI"), 200

@app.route("/manifest.json")
def manifest():
    return send_from_directory(BASE_DIR, "manifest.json", mimetype="application/manifest+json")

@app.route("/sw.js")
def service_worker():
    response = make_response(send_from_directory(BASE_DIR, "sw.js", mimetype="application/javascript"))
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route("/ads.txt")
def ads_txt():
    # Set ADS_TXT_CONTENT in Render environment variables after receiving
    # your publisher record from your ad network.
    content = os.environ.get("ADS_TXT_CONTENT", "").strip()
    if not content:
        content = "# Add your verified ad-network seller record here.\n"
    return Response(content + ("" if content.endswith("\n") else "\n"),
                    mimetype="text/plain")

@app.route("/icon.svg")
def icon():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
    <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#8b5cf6"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs>
    <rect width="512" height="512" rx="112" fill="#070913"/>
    <rect x="72" y="72" width="368" height="368" rx="92" fill="url(#g)"/>
    <path d="M156 340V172h52l48 72 48-72h52v168h-56V256l-44 64-44-64v84z" fill="#fff"/>
    <circle cx="374" cy="138" r="28" fill="#fff" opacity=".9"/>
    </svg>"""
    return Response(svg, mimetype="image/svg+xml")

@app.route("/<path:filename>")
def assets(filename):
    # Only serve the five project files and explicitly named static assets.
    allowed = {"index.html", "manifest.json", "sw.js", "requirements.txt"}
    if filename in allowed:
        return send_from_directory(BASE_DIR, filename)
    return jsonify(error="Not found"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
