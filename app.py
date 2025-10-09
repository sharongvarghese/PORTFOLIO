from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Project
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mysecretkey")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Home route
@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

# Hidden admin login
@app.route('/sharon_secret_admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.getenv('ADMIN_USER') and password == os.getenv('ADMIN_PASS'):
            session['admin'] = True
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials!", "danger")
    return render_template('admin_login.html', hide_navbar=True)

# Admin dashboard
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    projects = Project.query.all()
    return render_template('dashboard.html', projects=projects, hide_navbar=True)

# Add new project
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        new_project = Project(
            title=request.form['title'],
            description=request.form['description'],
            image=request.form['image'],
            link=request.form['link'],
            source=request.form['source']
        )
        db.session.add(new_project)
        db.session.commit()
        flash("Project added successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_edit_project.html', project=None, hide_navbar=True)

# Edit project
@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.image = request.form['image']
        project.link = request.form['link']
        project.source = request.form['source']
        db.session.commit()
        flash("Project updated successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_edit_project.html', project=project, hide_navbar=True)

# Delete project
@app.route('/delete_project/<int:id>', methods=['POST'])
def delete_project(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted successfully!", "success")
    return redirect(url_for('dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
