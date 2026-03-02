from flask import Blueprint, render_template

pages = Blueprint('pages', __name__, template_folder='../templates')

@pages.route('/login')
def login_page():
    return render_template('login.html')

@pages.route('/upload')
def upload_page():
    return render_template('upload.html')

@pages.route('/register')
def register_page():
    return render_template('register.html')