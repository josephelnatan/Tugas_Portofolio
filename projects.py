from flask import Blueprint, render_template, request, session, redirect
import pymysql
import cloudinary.uploader
import config

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/admin/proyek', methods=['GET', 'POST'])
def kelola_proyek():
    if not session.get('loggedin'):
        return redirect('/login')

    conn = config.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    edit_id = request.args.get('edit')
    proyek_edit = None

    if request.method == 'POST':
        judul = request.form.get('judul')
        deskripsi = request.form.get('deskripsi')
        link_proyek = request.form.get('link_proyek')
        foto = request.files.get('foto')
        post_edit_id = request.form.get('edit_id')  # ← ambil dari hidden input

        foto_url = None
        if foto and foto.filename != '':
            try:
                upload_result = cloudinary.uploader.upload(foto, folder="portofolio_proyek")
                foto_url = upload_result.get('secure_url')
            except Exception as e:
                print(f"Gagal upload ke Cloudinary: {e}")

        if post_edit_id:
            # ── MODE EDIT ──────────────────────────────────────────
            if foto_url:
                cursor.execute(
                    "UPDATE proyek SET judul=%s, deskripsi=%s, foto_url=%s, link_proyek=%s WHERE id=%s",
                    (judul, deskripsi, foto_url, link_proyek, post_edit_id)
                )
            else:
                # Foto tidak diganti, biarkan foto lama tetap ada
                cursor.execute(
                    "UPDATE proyek SET judul=%s, deskripsi=%s, link_proyek=%s WHERE id=%s",
                    (judul, deskripsi, link_proyek, post_edit_id)
                )
        else:
            # ── MODE TAMBAH BARU ───────────────────────────────────
            cursor.execute(
                "INSERT INTO proyek (judul, deskripsi, foto_url, link_proyek) VALUES (%s, %s, %s, %s)",
                (judul, deskripsi, foto_url or "", link_proyek)
            )

        conn.commit()
        return redirect('/admin/proyek')  # ← hindari re-submit saat refresh

    if edit_id:
        cursor.execute("SELECT * FROM proyek WHERE id=%s", (edit_id,))
        proyek_edit = cursor.fetchone()

    cursor.execute("SELECT * FROM proyek ORDER BY id DESC")
    data_proyek = cursor.fetchall()
    conn.close()

    return render_template(
        'admin/projects.html',
        daftar_proyek=data_proyek,
        proyek_edit=proyek_edit
    )


@projects_bp.route('/admin/proyek/hapus/<int:id>')
def hapus_proyek(id):
    if not session.get('loggedin'):
        return redirect('/login')

    conn = config.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proyek WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/proyek')