from flask import Blueprint, render_template, request, session, redirect

# Bikin blueprint khusus autentikasi
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['loggedin'] = True       
            session['username'] = username   
            return redirect('/admin/profil') 
        else:
            error = 'Username atau Password salah bro!'
            
    return render_template('admin/login.html', error=error)
    
@auth_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect('/login')