# coding=utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from iHome import create_app, db
from flask import session

app = create_app('DevelopmentConfig')
from iHome import redis_store
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/', methods=['POST', 'GET'])
def index():
    redis_store.set('name', '222')
    session['name'] = '111'
    return 'hello world'


if __name__ == '__main__':
    manager.run()
