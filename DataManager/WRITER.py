from app import db


class WRITER(db.Model):
    writerName = db.Column(db.NVARCHAR(50), primary_key=True)
    writerYear = db.Column(db.NVARCHAR(50))
    writerSchool = db.Column(db.NVARCHAR(50))
    writerTarget = db.Column(db.NVARCHAR(50))
