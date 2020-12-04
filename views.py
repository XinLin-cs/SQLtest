from flask import redirect
from flask import render_template
from flask import url_for
from flask import request
from app import app
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


@app.route('/controller')
def controller():
    return render_template(
        'controller.html',
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
    else:
        post_list = []
    return render_template(
        'viewer.html',
        post_list=post_list,
    )
