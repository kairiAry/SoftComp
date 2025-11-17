from flask import (
    Blueprint, render_template
)

latihan1_bp = Blueprint('latihan1', __name__, template_folder='templates')

@latihan1_bp.route('/')
def index():
    return render_template('halaman1.html')