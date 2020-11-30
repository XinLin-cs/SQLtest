from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import INT, NVARCHAR

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello-world-jcfuns'  # CSRF保护密钥
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://testServer:123456@sqltest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)


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


import views
if __name__ == '__main__':
    app.run(debug=True)
