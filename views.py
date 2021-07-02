from flask import redirect
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from sqlalchemy import func, desc

from app import app
from app import db
from DataManager.WRITER import WRITER
from DataManager.USER import USER
from DataManager.POST import POST
from DataManager.POST import POST_V


@app.route('/')
@app.route('/home')
def home():
    post_list = POST_V.query.order_by(POST_V.pop.desc()).all()
    next_url = url_for('home')
    return render_template(
        'index.html',
        web_tag='home',
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


@app.route('/controller_root', methods=['POST', 'GET'])
def controller_root():
    root_list = USER.query.all()
    return render_template(
        'controller_root.html',
        root_list=root_list,
    )


@app.route('/controller_writer', methods=['POST', 'GET'])
def controller_writer():
    writer_list = WRITER.query.all()
    return render_template(
        'controller_writer.html',
        writer_list=writer_list,
    )


@app.route('/viewer', methods=['post', 'get'])
def viewer():
    searchType = request.form.get('searchType')
    searchTarget = request.form.get('searchTarget')
    if searchType == '标题':
        res = POST.query.filter(POST.postTitle.like("%"+searchTarget+"%"))
    elif searchType == '内容':
        res = POST.query.filter(POST.postContent.like("%"+searchTarget+"%"))
    elif searchType == '作者':
        res = POST.query.filter(POST.writerName.like("%"+searchTarget+"%"))
    elif searchType == '现在学校':
        res = POST.query.filter(POST.writerSchool.like("%"+searchTarget+"%"))
    elif searchType == '目标院校':
        res = POST.query.filter(POST.writerTarget.like("%"+searchTarget+"%"))
    else:
        pass
    post_list = res.all()
    res_cnt = res.count()
    return render_template(
        'viewer.html',
        post_list=post_list,
        searchType=searchType,
        searchTarget=searchTarget,
        res_cnt=res_cnt,
    )


@app.route('/detail_post/<postID>', methods=['post', 'get'])
def detail_post(postID):
    post = POST.query.filter(POST.ID == postID).first()
    if post is not None:
        if post.writerYear is None:
            post.writerYear = 0
    return render_template(
        'detail_post.html',
        post=post,
    )


@app.route('/update_post', methods=['post', 'get'])
def update_post():
    ID = request.form.get('ID')
    url = request.form.get('url')
    postTime = request.form.get('postTime')
    postTitle = request.form.get('postTitle')
    postContent = request.form.get('postContent')
    writerName = request.form.get('writerName')
    writerYear = request.form.get('writerYear')
    writerSchool = request.form.get('writerSchool')
    writerTarget = request.form.get('writerTarget')
    session = db.session
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
    session.close()
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
    session.close()
    return redirect(url_for('controller_post'))


@app.route('/overview')
def overview():
    session = db.session
    likes_sum = POST.query.with_entities(func.sum(POST.likes)).first()[0]
    likes_max = POST.query.with_entities(func.max(POST.likes)).first()[0]
    likes_avg = POST.query.with_entities(func.avg(POST.likes)).first()[0]
    favor_sum = POST.query.with_entities(func.sum(POST.favorites)).first()[0]
    favor_max = POST.query.with_entities(func.max(POST.favorites)).first()[0]
    favor_avg = POST.query.with_entities(func.avg(POST.favorites)).first()[0]
    add_sum = POST.query.with_entities(func.sum(POST.additions)).first()[0]
    add_max = POST.query.with_entities(func.max(POST.additions)).first()[0]
    school_list = \
        session.query(func.count(POST.writerSchool), POST.writerSchool)\
        .group_by(POST.writerSchool)\
        .having(POST.writerSchool != "")\
        .order_by(func.count(POST.writerSchool).desc())\
        .limit(10).all()
    target_list = \
        session.query(func.count(POST.writerTarget), POST.writerTarget) \
        .group_by(POST.writerTarget)\
        .having(POST.writerTarget != "")\
        .order_by(func.count(POST.writerTarget).desc())\
        .limit(10).all()
    year_list = \
        session.query(func.count(POST.writerYear), POST.writerYear) \
        .group_by(POST.writerYear)\
        .having(POST.writerYear != "")\
        .order_by(func.count(POST.writerYear).desc())\
        .limit(5).all()
    session.close()
    return render_template(
        'overview.html',
        web_tag='overview',
        likes_sum=likes_sum,
        likes_max=likes_max,
        likes_avg=likes_avg,
        favor_sum=favor_sum,
        favor_max=favor_max,
        favor_avg=favor_avg,
        add_sum=add_sum,
        add_max=add_max,
        school_list=school_list,
        target_list=target_list,
        year_list=year_list,

    )


@app.route('/login/?<string:msg>')
def login(msg):
    return render_template(
        'login.html',
        msg=msg,
    )


@app.route('/login_int', methods=['POST', 'GET'])
def login_int():
    username = request.form.get('uid')
    password = request.form.get('password')
    user = USER.query.filter(USER.name == username).first()
    if user is not None:
        if user.password == password:
            session['uid'] = user.ID
            session.permanent = True  # 是否保存用户登录状态
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login', msg="密码错误"))
    else:
        return redirect(url_for('login', msg="用户不存在"))


@app.context_processor
def my_context_processor():
    uid = session.get('uid')
    return {'uid': uid}


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
