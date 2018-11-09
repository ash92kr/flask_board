from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Post(db.Model):   # 테이블을 만드는 함수
# SQLAlchemy의 속성인 Model을 Post에 상속시킴

    # 데이터베이스 테이블 설정
    __tablename__='posts'  # 테이블
    id = db.Column(db.Integer, primary_key=True)   # 컬럼 식별자 지정(숫자) -> 생성될 때마다 식별자로서의 기능을 함
    title = db.Column(db.String, nullable=False)  # 제목은 null값이 되지 못함 -> null이 되면 저장 불가
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='post')
    
    # 생성자
    def __init__(self, title, content):  # post를 인스턴스화하면서 사용자가 입력한 제목이나 내용을 저장함
        self.title = title   # self.title은 위쪽의 title, 나머지 title 2개는 동일함
        self.content = content
        self.created_at = datetime.datetime.now()

# Model = 사용자가 입력한 내용을 저장하는 공간


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))   # 위에서 만든 테이블명_컬럼명과 연결
    created_at = db.Column(db.DateTime)
    creator = db.Column(db.String)
    
    def __init__(self, content, creator):
        self.content = content
        self.created_at = datetime.datetime.now()  # 생성자로 넣는 것이 아니라 자동으로 만들어짐
        self.creator = creator
