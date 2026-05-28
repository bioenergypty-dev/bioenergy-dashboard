from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

app = Flask(__name__)

# CLAVE SECRETA
app.secret_key = "bioenergy_secret_key_2025"

# CONFIG LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# USUARIOS
USERS = {
    "admin": {
        "password": "1234"
    }
}

# CLASE USUARIO
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# CARGAR USUARIO
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    # SI YA INICIÓ SESIÓN
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = USERS.get(username)

        if user and user["password"] == password:

            login_user(User(username))

            return redirect(url_for("home"))

        flash("Usuario o contraseña incorrectos")

    return render_template("login.html")

# HOME
@app.route("/")
@login_required
def home():

    return render_template(
        "index.html",
        user=current_user.id
    )

# LOGOUT
@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))

# EJECUTAR
if __name__ == "__main__":
    app.run(debug=True)
    