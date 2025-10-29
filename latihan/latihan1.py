from flask import Blueprint, render_template

latihan1_bp = Blueprint('latihan1', __name__)

@latihan1_bp.route('/latihan1')
def halaman_latihan_1():
    return render_template('halaman1.html')