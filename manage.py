from flask import render_template, request
from flask_migrate import MigrateCommand
from flask_script import Manager

from App import create_app

# App __init__.py
app = create_app()

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
