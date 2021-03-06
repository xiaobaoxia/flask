# coding=utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from iHome import create_app, db
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


app = create_app('DevelopmentConfig')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    manager.run()
