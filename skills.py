from flask import Blueprint, render_template, request, session, redirect
import pymysql
import config

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/admin/skill', methods=['GET', 'POST'])
def kelola_skill():
    if not session.get('loggedin'):
        return redirect('/login')

    conn = config.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    edit_id = request.args.get('edit')
    skill_edit = None

    if request.method == 'POST':
        nama_skill = request.form.get('nama_skill')
        tingkat = request.form.get('tingkat')
        post_edit_id = request.form.get('edit_id')

        if post_edit_id:
            cursor.execute(
                "UPDATE skill SET nama_skill=%s, tingkat=%s WHERE id=%s",
                (nama_skill, tingkat, post_edit_id)
            )
        else:
            cursor.execute(
                "INSERT INTO skill (nama_skill, tingkat) VALUES (%s, %s)",
                (nama_skill, tingkat)
            )

        conn.commit()
        return redirect('/admin/skill')

    if edit_id:
        cursor.execute("SELECT * FROM skill WHERE id=%s", (edit_id,))
        skill_edit = cursor.fetchone()

    cursor.execute("SELECT * FROM skill ORDER BY id DESC")
    data_skill = cursor.fetchall()
    conn.close()

    return render_template('admin/skills.html', daftar_skill=data_skill, skill_edit=skill_edit)


@skills_bp.route('/admin/skill/hapus/<int:id>')
def hapus_skill(id):
    if not session.get('loggedin'):
        return redirect('/login')

    conn = config.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM skill WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/skill')
