from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import APP
from models import db


#----------------------------------------------------------------------------#
# Database Manage & Migrations on Heroku.

# to run the migrate on db:
# python3 manage.py db init
# python3 manage.py db migrate
# python3 manage.py db upgrade
#----------------------------------------------------------------------------#

migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
