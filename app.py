from flask import Flask, render_template, jsonify
from api.books import books_bp
from docs.swagger import swagger_ui_blueprint, API_URL_FOR_SWAGGER_UI, SWAGGER_JSON_DATA
from config import Config

print("--- App startup: Starting create_app() function ---")


def create_app():
    app = Flask(__name__, template_folder='templates')  # Specify template folder
    app.config.from_object(Config)

    print(f"--- App startup: Flask app created with config. DEBUG: {app.debug} ---")
    print(f"--- App startup: Database URI: {app.config['SQLALCHEMY_DATABASE_URI']} ---")

    app.register_blueprint(books_bp)
    app.register_blueprint(swagger_ui_blueprint)
    print("--- App startup: Blueprints registered ---")

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route(API_URL_FOR_SWAGGER_UI)
    def serve_openapi_spec():
        print(f"--- API Debug: Serving OpenAPI JSON from {API_URL_FOR_SWAGGER_UI} ---")
        return jsonify(SWAGGER_JSON_DATA)

    print("--- App startup: create_app() function finished, returning app instance ---")
    return app


if __name__ == '__main__':
    print("--- Running app directly (not via Gunicorn) ---")
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
