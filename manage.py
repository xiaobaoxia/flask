# coding=utf-8
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
manager = Manager(app)
db = SQLAlchemy(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run()
