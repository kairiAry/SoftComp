from flask import Flask, render_template
from latihan.latihan1 import latihan1_bp

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Daftarkan Blueprint ke aplikasi utama
app.register_blueprint(latihan1_bp)

# Rute untuk halaman utama (Home)
@app.route("/")
def index():
    return render_template('index.html')

# Jalankan server
if __name__ == "__main__":
    app.run(debug=True)