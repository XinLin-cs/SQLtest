from flask import redirect
from flask import render_template
from flask import url_for
from flask import request
from app import app
from app import db
from DataManager.POST import POST
from datetime import datetime


@app.route('/')
@app.route('/home/<page>')
def home(page=1):
    page = int(page)
    left_id = page*20+1
    right_id = page*20+20
    post_list = POST.query.filter(POST.ID >= left_id)\
        .filter(POST.ID <= right_id).all()
    next_url = url_for('home', page=page+1)
    return render_template(
        'index.html',
        page=page,
        post_list=post_list,
        next_url=next_url,
    )


@app.route('/jmpPage/<page>', methods=['GET'])
def get_data(page):
    return redirect(url_for('home', page=page))


@app.route('/controller_post', methods=['POST', 'GET'])
def controller_post():
    if 'searchType' in request.form:
        searchType = request.form.get('searchType')
        searchTarget = request.form.get('searchTarget')
        if searchType == '标题':
            post_list = POST.query.filter(POST.postTitle.like("%" + searchTarget + "%")).all()
        elif searchType == '内容':
            post_list = POST.query.filter(POST.postContent.like("%" + searchTarget + "%")).all()
        elif searchType == '作者':
            post_list = POST.query.filter(POST.writerName.like("%" + searchTarget + "%")).all()
        elif searchType == '现在学校':
            post_list = POST.query.filter(POST.writerSchool.like("%" + searchTarget + "%")).all()
        elif searchType == '目标院校':
            post_list = POST.query.filter(POST.writerTarget.like("%" + searchTarget + "%")).all()
        else:
            post_list = []
    else:
        post_list = POST.query.all()
    return render_template(
        'controller_post.html',
        post_list=post_list,
    )


@app.route('/viewer', methods=['post', 'get'])
def viewer():
    searchType = request.form.get('searchType')
    searchTarget = request.form.get('searchTarget')
    if searchType == '标题':
        post_list = POST.query.filter(POST.postTitle.like("%"+searchTarget+"%")).all()
    elif searchType == '内容':
        post_list = POST.query.filter(POST.postContent.like("%"+searchTarget+"%")).all()
    elif searchType == '作者':
        post_list = POST.query.filter(POST.writerName.like("%"+searchTarget+"%")).all()
    elif searchType == '现在学校':
        post_list = POST.query.filter(POST.writerSchool.like("%"+searchTarget+"%")).all()
    elif searchType == '目标院校':
        post_list = POST.query.filter(POST.writerTarget.like("%"+searchTarget+"%")).all()
    else:
        post_list = []
    return render_template(
        'viewer.html',
        post_list=post_list,
        searchType=searchType,
        searchTarget=searchTarget,
    )


@app.route('/detail_post/<postID>', methods=['post', 'get'])
def detail_post(postID):
    post = POST.query.filter(POST.ID == postID).first()
    return render_template(
        'detail_post.html',
        post=post,
    )


@app.route('/update_post', methods=['post', 'get'])
def update_post():
    session = db.session
    ID = request.form.get('ID')
    url = request.form.get('url')
    postTime = request.form.get('postTime')
    postTitle = request.form.get('postTitle')
    postContent = request.form.get('postContent')
    writerName = request.form.get('writerName')
    writerYear = request.form.get('writerYear')
    writerSchool = request.form.get('writerSchool')
    writerTarget = request.form.get('writerTarget')

    post = POST.query.filter_by(ID=ID).first()
    if post is None:
        post = POST(ID=ID, url=url, postTime=postTime, postTitle=postTitle,
                    postContent=postContent, writerName=writerName, writerYear=writerYear,
                    writerSchool=writerSchool, writerTarget=writerTarget)
        session.add(post)
    else:
        post.ID = ID
        post.postTime = postTime
        post.postTitle = postTitle
        post.postContent = postContent
        post.writerName = writerName
        post.writerYear = writerYear
        post.writerSchool = writerSchool
        post.writerTarget = writerTarget
    session.commit()
    return redirect(url_for('controller_post'))


@app.route('/delete_post/<postID>', methods=['post', 'get'])
def delete_post(postID):
    session = db.session
    post = POST.query.filter_by(ID=postID).first()
    if post is None:
        pass
    else:
        session.delete(post)
    session.commit()
    return redirect(url_for('controller_post'))
