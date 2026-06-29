from flask import Blueprint, render_template, request, session, redirect
import pymysql
import config

experience_bp = Blueprint('experience', __name__)

@experience_bp.route('/admin/pengalaman', methods=['GET', 'POST'])
def kelola_pengalaman():
    if not session.get('loggedin'):
        return redirect('/login')

    conn = config.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    edit_id = request.args.get('edit')
    pengalaman_edit = None

    if request.method == 'POST':
        posisi = request.form.get('posisi')
        perusahaan = request.form.get('perusahaan')
        tahun = request.form.get('tahun')
        deskripsi = request.form.get('deskripsi')
        post_edit_id = request.form.get('edit_id')

        if post_edit_id:
            cursor.execute(
                "UPDATE pengalaman SET posisi=%s, perusahaan=%s, tahun=%s, deskripsi=%s WHERE id=%s",
                (posisi, perusahaan, tahun, deskripsi, post_edit_id)
            )
        else:
            cursor.execute(
                "INSERT INTO pengalaman (posisi, perusahaan, tahun, deskripsi) VALUES (%s, %s, %s, %s)",
                (posisi, perusahaan, tahun, deskripsi)
            )

        conn.commit()
        return redirect('/admin/pengalaman')

    if edit_id:
        cursor.execute("SELECT * FROM pengalaman WHERE id=%s", (edit_id,))
        pengalaman_edit = cursor.fetchone()

    cursor.execute("SELECT * FROM pengalaman ORDER BY id DESC")
    data_pengalaman = cursor.fetchall()
    conn.close()

    return render_template('admin/experience.html', daftar_pengalaman=data_pengalaman, pengalaman_edit=pengalaman_edit)


@experience_bp.route('/admin/pengalaman/hapus/<int:id>')
def hapus_pengalaman(id):
    if not session.get('loggedin'):
        return redirect('/login')

    conn = config.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pengalaman WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/pengalaman')
