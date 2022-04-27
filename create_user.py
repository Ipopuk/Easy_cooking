from webapp import create_app
from webapp.user.models import User
from webapp.db import db

app = create_app()
with app.app_context():
    new_user = User(username='vasya', email='example@example.com')
    new_user.set_password('123')
    db.session.add(new_user)
    db.session.commit()
