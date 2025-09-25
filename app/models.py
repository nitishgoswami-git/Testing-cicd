from app import db

class User(db.Model):
    __tablename__ = "user"  # lowercase
    id = db.Column(db.Integer , primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)  # bigger for hashed pw