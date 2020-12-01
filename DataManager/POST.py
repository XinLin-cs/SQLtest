from app import db


class POST(db.Model):
    ID = db.Column(db.INT(), primary_key=True)
    url = db.Column(db.NVARCHAR(50), )
    postTime = db.Column(db.NVARCHAR(50))
    postTitle = db.Column(db.NVARCHAR(50))
    postContent = db.Column(db.NVARCHAR(200))
    watches = db.Column(db.INT())
    replies = db.Column(db.INT())
    favorites = db.Column(db.INT())
    likes = db.Column(db.INT())
    dislikes = db.Column(db.INT())
    additions = db.Column(db.INT())
    writerName = db.Column(db.NVARCHAR(50))
    writerYear = db.Column(db.NVARCHAR(50))
    writerSchool = db.Column(db.NVARCHAR(50))
    writerTarget = db.Column(db.NVARCHAR(50))
