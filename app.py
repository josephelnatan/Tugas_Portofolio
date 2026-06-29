from flask import Flask, render_template, request, session, redirect, url_for
import resend
import config 
import os
import pymysql
import cloudinary
from dotenv import load_dotenv

# --- IMPORT SEMUA BLUEPRINT YANG UDAH KITA BUAT ---
from auth import auth_bp
from dashboard import dashboard_bp
from projects import projects_bp
from skills import skills_bp
from experience import experience_bp

load_dotenv()

app = Flask(__name__, template_folder='frontend')
app.secret_key = 'portofolio_rahasia_123'

# Konfigurasi Cloudinary secara global
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# --- DAFTARKAN SEMUA BLUEPRINT KE FLASK ---
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(experience_bp)


# =======================================================
# --- RUTE FRONTEND UTAMA ---
# =======================================================
@app.route('/')
def home():
    conn = config.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # 1. Ambil data profil
    cursor.execute("SELECT * FROM profil LIMIT 1")
    data_profil = cursor.fetchone()
    
    # 2. Ambil data proyek
    cursor.execute("SELECT * FROM proyek ORDER BY id DESC")
    data_proyek = cursor.fetchall()
    
    # 3. Ambil data skill
    cursor.execute("SELECT * FROM skill ORDER BY id DESC")
    data_skill = cursor.fetchall()
    
    # 4. Ambil data pengalaman
    cursor.execute("SELECT * FROM pengalaman ORDER BY id DESC")
    data_pengalaman = cursor.fetchall()
    
    conn.close()
    
    # Kirim semua data ke halaman index.html
    return render_template('utama/index.html', 
                           profil=data_profil, 
                           daftar_proyek=data_proyek, 
                           daftar_skill=data_skill, 
                           daftar_pengalaman=data_pengalaman)


# =======================================================
# KODE UNTUK PROSES EMAIL (RESEND API)
# =======================================================
@app.route('/kirim-pesan', methods=['POST'])
def kirim_pesan():
    nama = request.form.get('nama')
    email_pengirim = request.form.get('email')
    pesan = request.form.get('pesan')
    
    resend.api_key = os.getenv("RESEND_API_KEY")
    
    try:
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "jlnatans05@gmail.com", 
            "subject": f"Pesan Baru Portofolio dari {nama}",
            "html": f"""
                <h3>Ada pesan baru di website portofolio kamu!</h3>
                <p><strong>Nama Pengirim:</strong> {nama}</p>
                <p><strong>Email Pengirim:</strong> {email_pengirim}</p>
                <p><strong>Isi Pesan:</strong></p>
                <p>{pesan}</p>
            """
        })
        return """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pesan Terkirim</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light d-flex align-items-center justify-content-center" style="min-height: 100vh;">
    <div class="text-center p-5 bg-white rounded shadow" style="max-width: 500px;">
        <div style="font-size: 60px;">✅</div>
        <h3 class="fw-bold mt-3">Pesan Terkirim!</h3>
        <p class="text-muted">Terima kasih telah menghubungi saya. Saya akan segera membalas pesan anda.</p>
        <a href="/" class="btn btn-primary mt-3 fw-bold">← Kembali ke Halaman Utama</a>
    </div>
</body>
</html>
"""
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
        return f"<h1>❌ Gagal mengirim pesan. Eror: {e}</h1>"


# TOMBOL ON FLASK
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)