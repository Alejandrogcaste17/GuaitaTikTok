from pymongo import MongoClient

# Configura la URI de MongoDB
mongo_uri = 'mongodb+srv://alejandrogcaste17:guaitaTikTok@guaitatiktok.ouggjsa.mongodb.net/'

# Crea un cliente MongoDB
client = MongoClient(mongo_uri)

# Selecciona la base de datos que usarás
db = client.GuaitaTikTok
usersCollection = db.users
tasksCollection = db.tasks
videosCollection = db.videos
profilesCollection = db.profiles