from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *   # models.py의 내용 전체를 불러온다
import os

app = Flask(__name__)  # flask를 가장 처음 만들 때 적어야 한다

# DB 설정
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///board'   # 내가 설정한 DB이름으로 적기
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(('DATABASE_URL'))   # heroku에서 DB를 가져오기 위해서 상수가 아닌 변수로 URL 주소 지정
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)   # models.py에서 설정한 db를 가져옴
migrate = Migrate(app, db)

# 루트로 가면 나올 hello 주소
# READ 기능 - 개별 post 출력 or 전체 post 출력
@app.route('/')
def index():
    # posts = Post.query.all()  # SELECT * FROM posts;
    posts = Post.query.order_by(Post.id.desc()).all()  # id의 내림차순으로 보여줌(기본 오름차순)  SELECT * FROM posts ORDER BY id DESC;
    return render_template('index.html', posts=posts)  # post를 전부 가져와서 index.html에 posts와 같이 넘긴다


@app.route('/posts/new')   # 사용자가 입력하는 폼
def new():
    return render_template('new.html')   # 이 주소에는 사용자가 입력할 수 있는 폼만 만들면 된다


# db에 저장하기 위해서는 사용자가 데이터를 입력해야 한다 - create
@app.route('/posts/create', methods = ["POST"])  # 이 요청이 들어오면 create 행동을 실시함
def create(): 
    # title = request.args.get('title')    # 서버에서 받아들이도록 가공해야 함
    # content = request.args.get('content')
    title = request.form.get("title")
    content = request.form.get("content")
    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()  # db에 사용자 데이터를 저장함
    
#   return render_template('create.html', post=post)  # post도 같이 보냄
    return redirect('/posts/{}'.format(post.id))   # post.id로 바로 보낸다


# 읽기(read)
@app.route('/posts/<int:id>')  # integer 형식만 받고, id만 들어올 수 있다(사용자가 요청하는 주소를 route가 받음)
def read(id):   # int로 받은 id를 read에 전달함 - read 메소드 실행
    post = Post.query.get(id)  # 가지고 올 id를 찾아 post에 저장  SELECT * FROM posts WHERE id=1;
    comments = Comment.query.all()  # 모든 카드에 모든 댓글을 보여준다
    
    return render_template('read.html', post=post)  # id와 post를 같이 read.html에 전달


# 삭제(delete)
@app.route('/posts/<int:id>/delete')
def delete(id):
    post = Post.query.get(id)   # 특정 id를 가진 문서를 찾아 post에 담고 전달함
    db.session.delete(post)   # read에 있는 문장
    db.session.commit()   # update에 있는 문장
    # DELETE FROM posts WHERE id=3;

    return redirect('/')  # 항목을 삭제한 다음, 원래 루트 페이지로 돌아간다


# 수정(update)
@app.route('/posts/<int:id>/edit')
def edit(id):
    post = Post.query.get(id)   # read 방식과 동일
    return render_template('edit.html', post=post)   # 단순히 불러오는 것이므로 똑같은 위치를 만들어야 한다


@app.route('/posts/<int:id>/update', methods=["POST"])
def update(id):
    post = Post.query.get(id)   # 새로운 객체를 만드는 것이 아니라 기존 것을 불러오면 된다
    # post.title = request.args.get("title")
    # post.content = request.args.get("content")  # title과 content를 사용자가 입력한 값으로 바꿈
    post.title = request.form.get("title")
    post.content = request.form.get("content")
    db.session.commit()   # 바꾼 값을 commit만 하면 됨
    return redirect('/posts/{}'.format(id))   # {{ }}는 html 내에서 파이썬 코드를 넣을 때 사용 가능
     
# get 방식 사용자의 정보가 주소 표시줄에 실려서 나감 -> 어떤 데이터를 가져올 때 사용
# post 방식은 서버로 데이터를 보낼 때 사용 -> url에 아무 것도 찍히지 않고 ? 앞 부분의 주소만 출력됨      
     

# 댓글 기능 CR
@app.route("/posts/<int:post_id>/comments", methods=["POST"])  # post_id가 출력될 것
def comments(post_id):
    content = request.form.get('content')   # requests는 외부의 정보 크롤링할 때 사용함, content는 사용자가 입력한 댓글 -> get 방식
    creator = request.form.get('creator')
    comment = Comment(content, creator)   # Comment는 클래스를 생성하는 행위 -> 안의 content는 내부의 comment로 이동함

    post = Post.query.get(post_id)
    post.comments.append(comment)   # comments 테이블에 post_id를 알려주기 위해 추가

    db.session.add(comment)
    db.session.commit()
    
    return redirect('/')
    
    
# 댓글 삭제(delete)
@app.route('/comment/<int:id>/delete')
def comment_delete(id):
    comment = Comment.query.get(id)   # comment.id를 저장함

    db.session.delete(comment)  
    db.session.commit()
    return redirect('/')