from app import db


class USER(db.Model):
    ID = db.Column(db.INT(), primary_key=True)
    name = db.Column(db.NVARCHAR(45), )
    password = db.Column(db.NVARCHAR(45))
