from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure app
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///calculadora.db")

# Matérias
MATERIAS = ["lin", "hum", "nat", "mat", "red"]


@app.context_processor
def inject_variables():
    """
    Faz materias e usuario ficarem disponíveis em todos os templates

    https://flask.palletsprojects.com/en/2.1.x/templating/#context-processors
    """
    # Get username
    try:
        user_id = session["user_id"]
    except KeyError:
        user_id = None

    if user_id:
        rows = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        usuario = rows[0]["username"]
    else:
        usuario = None
    return dict(materias=MATERIAS, usuario=usuario)


@app.route("/")
def index():
    """Calculadora ENEM"""
    return render_template("index.html")


@app.route("/adicionar", methods=["POST"])
@login_required
def adicionar():
    """Salvar notas e pesos"""

    # Saber se é para salvar como nota ou peso
    selecionado = request.form.get("selecionado")

    # Confirmar se dados não estão em branco
    user_id = session["user_id"]
    if not user_id:
        flash("Para realizar essa ação é necessário estar logado.", "error")
        return render_template("login.html", username_attribute="autofocus")

    nome = request.form.get("name")
    if not nome:
        flash("Há dados em branco.", "error")
        return render_template("notas-e-pesos.html")

    # Salvar notas na base de dados
    if selecionado == "Notas":

        # Confirmar se não há notas com esse nome
        if db.execute("SELECT * FROM notas WHERE user_id = ? AND nome = ?", user_id, nome):
            flash("Já há dados salvos com esse nome.", "error")
            return render_template("notas-e-pesos.html")
        else:
            db.execute("INSERT INTO notas (user_id, nome) VALUES (?, ?)", user_id, nome)

        for materia in MATERIAS:
            nota_materia = f"nota_{materia}"
            nota = request.form.get(f"nota-{materia}")
            db.execute("UPDATE notas SET ? = ? WHERE user_id = ? AND nome = ?", nota_materia, nota, user_id, nome)
        flash("Notas salvas.", "success")

    # Salvar pesos na base de dados
    elif selecionado == "Pesos":

        # Confirmar se não há pesos com esse nome (curso)
        if db.execute("SELECT * FROM pesos WHERE user_id = ? AND curso = ?", user_id, nome):
            flash("Já há dados salvos com esse nome.", "error")
            return render_template("notas-e-pesos.html")
        else:
            db.execute("INSERT INTO pesos (user_id, curso) VALUES (?, ?)", user_id, nome)

        for materia in MATERIAS:
            peso_materia = f"peso_{materia}"
            peso = request.form.get(f"peso-{materia}")
            db.execute("UPDATE pesos SET ? = ? WHERE user_id = ? AND curso = ?", peso_materia, peso, user_id, nome)
        flash("Pesos salvos.", "success")

    # Carregar dados e redirect to /notas-e-pesos
    rows = db.execute("SELECT * FROM ? WHERE user_id = ?", selecionado.lower(), session["user_id"])
    return render_template("notas-e-pesos.html", selecionado=selecionado, rows=rows)


@app.route("/adicionar-notas")
@login_required
def adicionar_notas():
    """Interface para adicionar notas"""
    return render_template("adicionar.html", selecionado="Notas")


@app.route("/adicionar-pesos")
@login_required
def adicionar_pesos():
    """Interface para adicionar pesos"""
    return render_template("adicionar.html", selecionado="Pesos")


@app.route("/alterar", methods=["GET", "POST"])
@login_required
def alterar():
    """Interface para alterar peso ou nota."""

    # Saber se é para alterar nota ou peso
    selecionado = request.form.get("selecionado")
    user_id = session["user_id"]
    notas = {}
    pesos = {}
    
    # Carregar dados a serem alterados (Notas)
    if selecionado == "Notas":
        notas["nome"] = request.form.get("nome")
        rows = db.execute("SELECT * FROM notas WHERE user_id = ? AND nome = ?", user_id, notas["nome"])
        
        if not rows:
            flash("Nota não encontrada.", "error")
            rows = db.execute("SELECT * FROM ? WHERE user_id = ?", selecionado.lower(), session["user_id"])
            return render_template("notas-e-pesos.html", selecionado=selecionado, rows=rows)
       
        for materia in MATERIAS:
            notas[materia] = rows[0][f"nota_{materia}"]

    # Carregar dados a serem alterados (Pesos)
    elif selecionado == "Pesos":
        pesos["curso"] = request.form.get("nome")
        rows = db.execute("SELECT * FROM pesos WHERE user_id = ? AND curso = ?", user_id, pesos["curso"])

        if not rows:
            flash("Peso não encontrado.", "error")
            rows = db.execute("SELECT * FROM ? WHERE user_id = ?", selecionado.lower(), session["user_id"])
            return render_template("notas-e-pesos.html", selecionado=selecionado, rows=rows)

        for materia in MATERIAS:
            pesos[materia] = rows[0][f"peso_{materia}"]

    return render_template("adicionar.html", titulo="Alterar", notas=notas, pesos=pesos, selecionado=selecionado)


@app.route("/atualizar", methods=["POST"])
@login_required
def atualizar():
    """Atualizar nota ou peso da base de dados."""

    # Saber qual nota ou peso alterar
    user_id = session["user_id"]
    selecionado = request.form.get("selecionado")
    nome_anterior = request.form.get("nome-anterior")
    
    # Checar dados
    if selecionado not in ["Notas", "Pesos"]:
        flash("Selecione Notas ou Pesos.", "error")
        return render_template("notas-e-pesos.html")
    if selecionado == "Notas":
        if not db.execute("SELECT * FROM notas WHERE user_id = ? AND nome = ?", user_id, nome_anterior):
            flash("Não foi possível encontrar nota.", "error")
            return render_template("notas-e-pesos.html")
    elif selecionado == "Pesos":
        if not db.execute("SELECT * FROM pesos WHERE user_id = ? AND curso = ?", user_id, nome_anterior):
            flash("Não foi possível encontrar peso.", "error")
            return render_template("notas-e-pesos.html")
    
    # Dados novos
    notas = {}
    pesos = {}
    nome = request.form.get("name")

    if selecionado == "Notas":
        for materia in MATERIAS:
            nota_materia = f"nota-{materia}"
            notas[materia] = request.form.get(nota_materia)

    elif selecionado == "Pesos":
        for materia in MATERIAS:
            peso_materia = f"peso-{materia}"
            pesos[materia] = request.form.get(peso_materia)

    # Atualizar banco de dados
    if selecionado == "Notas":
        for materia in MATERIAS:
            nota_materia = f"nota_{materia}"
            db.execute("UPDATE notas SET ? = ? WHERE user_id = ? AND nome = ?", nota_materia, notas[materia], user_id, nome_anterior)
        db.execute("UPDATE notas SET nome = ? WHERE user_id = ? AND nome = ?", nome, user_id, nome_anterior)
    elif selecionado == "Pesos":
        for materia in MATERIAS:
            peso_materia = f"peso_{materia}"
            db.execute("UPDATE pesos SET ? = ? WHERE user_id = ? AND curso = ?", peso_materia, pesos[materia], user_id, nome_anterior)
        db.execute("UPDATE pesos SET curso = ? WHERE user_id = ? AND curso = ?", nome, user_id, nome_anterior)

    flash("Dados alterados.", "success")    
    rows = db.execute("SELECT * FROM ? WHERE user_id = ?", selecionado.lower(), session["user_id"])
    return render_template("notas-e-pesos.html", selecionado=selecionado, rows=rows)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """Cadastrar usuário"""
    if request.method == "POST":
    
        # Check for username
        username = request.form.get("username")
        if not username:
            flash("Favor insira um nome de usuário.", "error")
            return render_template("cadastro.html", username_attribute="autofocus")

        # Check if username already exists
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            flash("Usuário já cadastrado ou nome já em uso.", "error")
            return render_template("cadastro.html", username_attribute="autofocus")

        # Password must be at least 4 characters long
        password = request.form.get("password")
        if len(password) < 4:
            flash("A senha precisa ter pelo menos 4 caracteres.", "error")
            return render_template("cadastro.html", username=username, password_attribute="autofocus")

        # Check for password confirmation
        confirm_password = request.form.get("confirm-password")
        if not confirm_password == password:
            flash("As senhas devem ser iguais.", "error")
            return render_template("cadastro.html", username=username, password_attribute="autofocus")
            
        # If no errors, register user to database
        password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", username, password)

        flash("Conta criada!", "success")
        return render_template("login.html", username=username, password_attribute="autofocus")

    return render_template("cadastro.html", username_attribute="autofocus")


@app.route("/excluir", methods=["POST"])
@login_required
def excluir():
    """Excluir nota ou peso da base de dados."""

    # Saber se é para excluir uma nota ou um peso
    selecionado = request.form.get("selecionado")

    # Informações para a exclusão
    user_id = session["user_id"]
    nome = request.form.get("nome")

    # Excluir nota
    if selecionado == "Notas":
        if not db.execute("SELECT * FROM notas WHERE user_id = ? AND nome = ?", user_id, nome):
            flash("Não foi possível encontrar nota.", "error")
            return redirect("/notas-e-pesos")
        db.execute("DELETE FROM notas WHERE user_id = ? AND nome = ?", user_id, nome)
        flash("Nota excluída.", "success")

    # Excluir peso
    elif selecionado == "Pesos":
        if not db.execute("SELECT * FROM pesos WHERE user_id = ? AND curso = ?", user_id, nome):
            flash("Não foi possível encontrar peso.", "error")
            return redirect("/notas-e-pesos")
        db.execute("DELETE FROM pesos WHERE user_id = ? AND curso = ?", user_id, nome)
        flash("Peso excluído.", "success")
    
    # Carregar dados e redirect to /notas-e-pesos
    rows = db.execute("SELECT * FROM ? WHERE user_id = ?", selecionado.lower(), session["user_id"])
    return render_template("notas-e-pesos.html", selecionado=selecionado, rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        
        # Check for username
        username = request.form.get("username")
        if not username:
            flash("Favor inserir um nome de usuário.", "error")
            return render_template("login.html", username_attribute="autofocus")

        # Check for password
        password = request.form.get("password")
        if not password:
            flash("Favor inserir sua senha.", "error")
            return render_template("login.html", username=username, password_attribute="autofocus")
        
        # Check if user is registered
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not rows:
            flash("Usuário não cadastrado.", "error")
            return render_template("login.html", username_attribute="autofocus")

        # Check if password and username match
        if not check_password_hash(rows[0]["password_hash"], password):
            flash("Senha incorreta.", "error")
            return render_template("login.html", username=username, password_attribute="autofocus")

        # If no errors, log user in
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    
    return render_template("login.html", username_attribute="autofocus")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/notas-e-pesos", methods=["GET", "POST"])
@login_required
def notas_e_pesos():
    """Display selected information"""
    if request.method == "POST":
        
        # Check for selected button
        selecionado = request.form.get("selected")
        if selecionado not in ["Notas", "Pesos"]:
            flash("Favor selecionar Notas ou Pesos.", "error")
            return render_template("notas-e-pesos.html")

        # Load data from database
        rows = db.execute("SELECT * FROM ? WHERE user_id = ?", selecionado.lower(), session["user_id"])
        return render_template("notas-e-pesos.html", selecionado=selecionado, rows=rows)

    # If requested via GET, load page
    return render_template("notas-e-pesos.html")


@app.route("/nova-senha", methods=["GET", "POST"])
def nova_senha():
    """Change password"""
    if request.method == "POST":

        # Keep track if there's an active session
        user_session = False

        # If no username input, either user is logged in or username is missing
        username = request.form.get("username")
        if not username:
            try:
                rows = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
            except KeyError:
                flash("Favor inserir um nome de usuário.", "error")
                return render_template("nova-senha.html", username_attribute="autofocus")
           
            # if rows:
            username = rows[0]["username"]
            user_session = True

        # New password must have at least 4 characters
        password = request.form.get("new-password")
        if len(password) < 4:
            flash("A nova senha precisa ter pelo menos 4 caracteres.")
            return render_template("nova-senha.html", password_attribute="autofocus")

        # Check for password confirmation
        confirm_password = request.form.get("confirm-password")
        if not confirm_password == password:
            flash("As senhas devem ser iguais", "error")

        # If no errors, change password
        password = generate_password_hash(password)
        db.execute("UPDATE users SET password_hash = ? WHERE username = ?", password, username)
        flash("Senha alterada.", "success")

        # If user is logged in
        if user_session:
            render_template("index.html")
        else:
            render_template("login.html", username_attribute="autofocus")

    return render_template("nova-senha.html", username_attribute="autofocus")

    
@app.route("/sobre-o-enem")
def sobre():
    """Sobre o ENEM"""
    return render_template("sobre.html")
    