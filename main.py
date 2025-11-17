import os
from flask import Flask, render_template
from latihan import register_blueprints

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

register_blueprints(app)

@app.route('/')
def home():
    """Halaman utama yang menampilkan daftar latihan."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)