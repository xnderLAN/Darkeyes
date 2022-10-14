from flask import Flask
from flask_mongoengine import MongoEngine
from apscheduler.schedulers.background import BackgroundScheduler

db = MongoEngine()

def create_app():
    global app 
    app= Flask(__name__)
    app.config["SECRET_KEY"] = "qwoioiooWWoLSK<55"
    app.config['SECURITY_PASSWORD_SALT'] = "next_key_Fuck_+you!!"

    app.config['MONGODB_SETTINGS'] = {
        'connect': False,
        #'host': 'mongodb://127.0.0.1:27017/Darky',
        'host': 'mongodb://db:27017/Darky'
    }
    
    db.init_app(app)

    from .api import api
    app.register_blueprint(api)
    from .views import views
    app.register_blueprint(views)
    
    from .darky import DarkyToreq, job

    from .models import Darckysources, Capture

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(job, 'interval', minutes=60)
    sched.start()
    
    return app
