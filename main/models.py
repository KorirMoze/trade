from main import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __rep__(self):
        return f"User('{self.userName}','{self.email}','{self.userImage}','{self.password}')"


class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Float(20), unique=True, nullable=False)
    productDescription = db.Column(db.String(300), nullable=False, default="default.jpg")

    def __rep__(self):
        return f"product('{self.productName}','{self.productDescription}','{self.productImage},'{self.price}')"
db.create_all()