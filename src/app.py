from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bson.objectid import ObjectId
from generalTaskAPI import process_general_task
from profileTaskAPI import process_profile_task
from mongoConfiguration import usersCollection, tasksCollection, videosCollection, statisticsCollection
from hashlib import sha256
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__, template_folder='../static/templates', static_folder='../static')
app.config['SECRET_KEY'] = '123456789012345678901234567890'

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
            hashed_password = sha256(password.encode()).hexdigest()
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
    hashed_password = sha256(password.encode()).hexdigest()

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

async def run_process_general_task(task_id, user_id):
    await process_general_task(task_id, user_id)

async def run_process_profile_task(task_id, user_id):
    await process_profile_task(task_id, user_id)

# Crear un ThreadPoolExecutor para tareas de fondo
executor = ThreadPoolExecutor(max_workers=4)

@app.route('/newTask')
@login_required
def newTask():
    return render_template('newTask.html',  username=current_user.username)

@app.route('/newTaskProfile', methods=['POST', 'GET'])
@login_required
def newTaskProfile():
    if request.method == 'POST':
        # Obtener los datos del formulario
        userProfile = request.form['username']
        taskName = request.form['name']
        description = request.form['description']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        language = request.form['language']

        if(startDate > endDate):
            # Mostrar un mensaje de éxito si el registro fue exitoso
            wrongDate = 'The end date is before the origin date, please change the values'
            return render_template('newTask.html', wrongDate=wrongDate, username=current_user.username)

        # Creamos nuestro documento a insertar en la base de datos
        task_document = {
            'state': 'In progress',
            'state_message': 'The task is currently being carried out',
            'userProfile': userProfile,
            'taskName': taskName,
            'description': description,
            'startDate': startDate,
            'endDate': endDate,
            'language': language,
            'userId': current_user.id,
            'taskType': 'profile'
        }

        # Insertar el documento en la colección de tasks
        result = tasksCollection.insert_one(task_document)
        
        # Verificar si la inserción fue exitosa
        if result.inserted_id:
            # Obtener el objeto completo insertado con su _id
            inserted_task = tasksCollection.find_one({'_id': result.inserted_id})

            # Ejecutar la tarea en segundo plano usando ThreadPoolExecutor
            executor.submit(asyncio.run, run_process_profile_task(inserted_task, current_user.id))

            # Mostrar un mensaje de éxito si el registro fue exitoso
            createdTask = 'The task has been created successfully, please go to the my tasks tab to see its status'
            return render_template('newTask.html', createdTask=createdTask, username=current_user.username)
        else:
            # Mostrar un mensaje de error si ocurrió un problema al insertar en la base de datos
            errorTask = 'Something strange happened, please try again.'
            return render_template('newTask.html', errorTask=errorTask, username=current_user.username)
        
    else:
        return render_template('newTask.html',  username=current_user.username)

@app.route('/newTaskGeneral', methods=['POST', 'GET'])
@login_required
def newTaskGeneral():
    if request.method == 'POST':
        # Obtener los datos del formulario
        taskName = request.form['name']
        description = request.form['description']
        tags = request.form['tags']
        keywords = request.form['keywords']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        language = request.form['language']

        if not tags and not keywords:
            # Mostrar un mensaje de error ya que no se completo alguno de los dos filtros
            notFilter = 'At least one of the two filters, "tags" or "keywords" must be filled'
            return render_template('newTask.html', notFilter=notFilter, username=current_user.username)

        # Convertir las etiquetas en un vector
        if tags:
            tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        else:
            tags_list = []

        # Convertir las palabras clave en un vector
        if keywords:
            keywords_list = [keyword.strip() for keyword in keywords.split(',') if keyword.strip()]
        else:
            keywords_list = []

        if(startDate > endDate):
            # Mostrar un mensaje de error ya que la fecha final es antes que la fecha de inicio
            wrongDate = 'The end date is before the origin date, please change the values'
            return render_template('newTask.html', wrongDate=wrongDate, username=current_user.username)
        
        # Creamos nuestro documento a insertar en la base de datos
        task_document = {
            'state': 'In progress',
            'state_message': 'The task is currently being carried out',
            'taskName': taskName,
            'description': description,
            'tags_list': tags_list,
            'keywords_list': keywords_list,
            'startDate': startDate,
            'endDate': endDate,
            'language': language,
            'userId': current_user.id,
            'taskType': 'general'
        }

        # Insertar el documento en la colección de tasks
        result = tasksCollection.insert_one(task_document)

        # Verificar si la inserción fue exitosa
        if result.inserted_id:
            # Obtener el objeto completo insertado con su _id
            inserted_task = tasksCollection.find_one({'_id': result.inserted_id})

            # Ejecutar la tarea en segundo plano usando ThreadPoolExecutor
            executor.submit(asyncio.run, run_process_general_task(inserted_task, current_user.id))

            # Mostrar un mensaje de éxito si el registro fue exitoso
            createdTask = 'The task has been created successfully, please go to the my tasks tab to see its status'
            return render_template('newTask.html', createdTask=createdTask, username=current_user.username)
        else:
            # Mostrar un mensaje de error si ocurrió un problema al insertar en la base de datos
            errorTask = 'Something strange happened, please try again.'
            return render_template('newTask.html', errorTask=errorTask, username=current_user.username)
    else:    
        return render_template('newTask.html',  username=current_user.username)

@app.route('/tasksView')
@login_required
def tasksView():

    # Verificar si el usuario ya existe en la base de datos
    existing_user_tasks = tasksCollection.find({'userId': current_user.id})
    
    # Convertir el cursor a una lista
    tasks_list = list(existing_user_tasks)

    if tasks_list:
        return render_template('tasksView.html', tasks_list=tasks_list, username=current_user.username)
    else:
        # Mostrar un mensaje de informacion de que no tiene tareas todavia creadas
        notTask = "Sorry, you don't have any tasks created yet, please go to the ""New Task"" section and start one."
        return render_template('tasksView.html', notTask=notTask, username=current_user.username)
    
@app.route('/taskReview/<task_id>')
@login_required
def taskReview(task_id):
    # Convertir task_id a ObjectId
    task_id = ObjectId(task_id)

    # Verificar si el usuario ya existe en la base de datos
    existing_task = tasksCollection.find_one({'_id': task_id})

    # Verificar si el usuario ya existe en la base de datos
    existing_user_tasks = tasksCollection.find({'userId': current_user.id})
    
    # Convertir el cursor a una lista
    tasks_list = list(existing_user_tasks)
    
    if existing_task['state'] == 'In progress':
        # Mostrar un mensaje de informacion de que todavia la tarea no ha terminado
        notFinished = "Sorry, you haven't finished the task yet, wait for it to finish to be able to access the review"
        return render_template('tasksView.html', tasks_list=tasks_list, notFinished=notFinished, username=current_user.username)
    
    if existing_task['state'] == 'Stopped':
        # Mostrar un mensaje de informacion de que no tiene tareas todavia creadas
        stopped = "Sorry, the task encountered an error while completing it, so the review option is not available."
        return render_template('tasksView.html', tasks_list=tasks_list, stopped=stopped, username=current_user.username)
    
    # Buscamos los videos relacionados con esa tarea
    videos = videosCollection.find_one({'taskId': task_id})

    statistics = statisticsCollection.find_one({'taskId': str(task_id)})

    if videos:
        return render_template('taskReview.html', task=existing_task, videos_list=videos, statistics=statistics, username=current_user.username)
    else:
        # Mostrar un mensaje de informacion de que no tiene tareas todavia creadas
        notVideoList = "I'm sorry, but there was a problem submitting the review request, please try again later."
        return render_template('taskReview.html', task=None, notVideoList=notVideoList, username=current_user.username)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
