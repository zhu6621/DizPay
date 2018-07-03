# -*- coding: utf-8 -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app
from app.api import init_api
from app.model import db

app = create_app()
init_api(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def db_initialize():
    from app.model.user import User
    User.initialize()


""" 使用说明
1. initialize
  python manage.py db init

2. migrate
  python manage.py db migrate
  python manage.py db upgrade

positional arguments:
  {upgrade,migrate,current,stamp,init,downgrade,history,revision}
    upgrade             Upgrade to a later version
    migrate             Alias for 'revision --autogenerate'
    current             Display the current revision for each database.
    stamp               'stamp' the revision table with the given revision;
                        dont run any migrations
    init                Generates a new migration
    downgrade           Revert to a previous version
    history             List changeset scripts in chronological order.
    revision            Create a new revision file.
"""

if __name__ == '__main__':
    manager.run()
