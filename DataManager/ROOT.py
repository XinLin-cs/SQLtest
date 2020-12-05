from app import db


class ROOT(db.Model):
    ID = db.Column(db.NVARCHAR(50), primary_key=True)
    password = db.Column(db.NVARCHAR(50))
