from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bson.objectid import ObjectId
import hashlib

app = Flask(__name__, template_folder='../static/templates', static_folder='../static')
app.config['SECRET_KEY'] = '123456789012345678901234567890'

# Configura la URI de MongoDB
mongo_uri = 'mongodb+srv://alejandrogcaste17:guaitaTikTok@guaitatiktok.ouggjsa.mongodb.net/'

# Crea un cliente MongoDB
client = MongoClient(mongo_uri)

# Selecciona la base de datos que usarás
db = client.GuaitaTikTok
usersCollection = db.users

# Configura Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    user_data = usersCollection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(id=str(user_data['_id']), username=user_data['username'], email=user_data['email'])
    return None

@app.route('/')
def main():
    return render_template('loginRegister.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar el usuario en la base de datos
        user_document = usersCollection.find_one({'email': email})

        if user_document:
            # Verificar la contraseña (hasheada)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == user_document['password']:
                user = User(id=str(user_document['_id']), username=user_document['username'], email=user_document['email'])
                login_user(user)
                # Redirigir a index.html si el inicio de sesión es exitoso
                return redirect(url_for('index'))
            else:
                # Mostrar un mensaje de error si la contraseña es incorrecta
                error = 'Wrong Password. Try Again.'
                return render_template('loginRegister.html', errorLogin=error)
        else:
            # Mostrar un mensaje de error si el usuario no existe
            error = 'User not found. Verify your User Name.'
            return render_template('loginRegister.html', errorLogin=error)
        
    return render_template('loginRegister.html')
    
@app.route('/registro', methods=['POST'])
def registro():
    # Obtener los datos del formulario
    username = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Opcional: Hashear la contraseña antes de almacenarla
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Verificar si el usuario ya existe en la base de datos
    existing_user = usersCollection.find_one({'email': email})

    if existing_user:
        # Mostrar un mensaje de error si el usuario ya existe
        error = 'This user is already registered.'
        return render_template('loginRegister.html', errorRegister=error)
    else:
        # Crear un documento para insertar en MongoDB
        user_document = {
            'username': username,
            'email': email,
            'password': hashed_password  # Almacenar la contraseña hasheada
        }

        # Insertar el documento en la colección de usuarios
        result = usersCollection.insert_one(user_document)

        # Verificar si la inserción fue exitosa
        if result.inserted_id:
            # Mostrar un mensaje de éxito si el registro fue exitoso
            correctRegister = 'The user registered successfully!'
            return render_template('loginRegister.html', correctRegister=correctRegister)
        else:
            # Mostrar un mensaje de error si ocurrió un problema al insertar en la base de datos
            errorDatabase = 'Something strange happened, please try again.'
            return render_template('loginRegister.html', errorDatabase=errorDatabase)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html',  username=current_user.username)

@app.route('/newTask')
@login_required
def newTask():
    return render_template('newTask.html',  username=current_user.username)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
