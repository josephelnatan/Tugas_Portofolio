from flask import Blueprint, render_template, request, session, redirect
import pymysql
import cloudinary.uploader
import config

# Bikin blueprint khusus dashboard profil
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/admin/profil', methods=['GET', 'POST'])
def kelola_profil():
    if not session.get('loggedin'):
        return redirect('/login')

    conn = config.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        nama = request.form.get('nama')
        deskripsi = request.form.get('deskripsi')
        foto = request.files.get('foto')
        
        cursor.execute("SELECT foto_url FROM profil LIMIT 1")
        profil_lama = cursor.fetchone()
        foto_url = profil_lama['foto_url'] if profil_lama else ""

        if foto and foto.filename != '':
            try:
                upload_result = cloudinary.uploader.upload(foto, folder="portofolio")
                foto_url = upload_result.get('secure_url')
            except Exception as e:
                print(f"Gagal upload ke Cloudinary: {e}")

        if profil_lama:
            cursor.execute("UPDATE profil SET nama = %s, deskripsi = %s, foto_url = %s WHERE id = 1", (nama, deskripsi, foto_url))
        else:
            cursor.execute("INSERT INTO profil (nama, deskripsi, foto_url) VALUES (%s, %s, %s)", (nama, deskripsi, foto_url))
        
        conn.commit()

    cursor.execute("SELECT * FROM profil LIMIT 1")
    data_profil = cursor.fetchone()
    conn.close()
    
    return render_template('admin/dashboard.html', profil=data_profil)