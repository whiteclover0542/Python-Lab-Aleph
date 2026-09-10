from datetime import datetime

from extensions import db


class Post(db.Model):
  """Aegis Access Lab 전체 게시판 글 — 등급과 무관하게 로그인만 하면 누구나 쓸 수 있다.

  (골드/관리자 페이지와 대조되는 '등급 체크 없는' 기준선 역할)
  """
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  content = db.Column(db.Text, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  author = db.relationship(
      'User', backref=db.backref('posts', lazy=True, cascade='all, delete-orphan'))
  created_at = db.Column(db.DateTime, default=datetime.now)

  def to_dict(self):
    return {
        'id': self.id,
        'title': self.title,
        'content': self.content,
        'author': self.author.username,
        'author_id': self.author_id,
        'created_at': self.created_at.isoformat() if self.created_at else None,
    }
