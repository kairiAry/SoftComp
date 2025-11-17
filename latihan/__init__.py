def register_blueprints(app):
    from .latihan1 import latihan1_bp
    from .latihan2 import latihan2_bp
    
    app.register_blueprint(latihan1_bp, url_prefix='/latihan1')
    app.register_blueprint(latihan2_bp, url_prefix='/latihan2')