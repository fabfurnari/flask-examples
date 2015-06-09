#!/usr/bin/env python

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
from testapp import app, db

db.create_all()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
manager.add_command("db", MigrateCommand)
manager.run()
