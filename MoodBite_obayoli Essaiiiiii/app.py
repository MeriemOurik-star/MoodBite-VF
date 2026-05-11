"""
app.py — MoodBite Flask Entry Point
"""
 
from flask import Flask, session, redirect, request
from whitenoise import WhiteNoise
from config import config, FIREBASE_CONFIG
 
from controllers.client_controller    import client_bp
from controllers.mood_controller      import mood_bp
from controllers.order_controller     import order_bp
from controllers.dashboard_controller import dashboard_bp
 
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
 
# Serve static files correctly on Railway/Gunicorn
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static')
 
app.register_blueprint(client_bp)
app.register_blueprint(mood_bp)
app.register_blueprint(order_bp)
app.register_blueprint(dashboard_bp)
 
# ── Language switcher route ──────────────────────────────────────────────────
@app.route("/lang/<lang_code>")
def switch_lang(lang_code):
    if lang_code in config.SUPPORTED_LANGS:
        session["lang"] = lang_code
    return redirect(request.referrer or "/")
 
# ── Context processor ────────────────────────────────────────────────────────
@app.context_processor
def inject_globals():
    lang = session.get("lang", config.DEFAULT_LANG)
    return {
        "lang":            lang,
        "fr":              lang == "fr",
        "firebase_config": FIREBASE_CONFIG,
        "mood_meta":       config.MOOD_META,
        "supported_moods": config.SUPPORTED_MOODS,
    }
 
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
 