from datetime import datetime

from constants import ROLE_GENERAL, ROLE_NAMES
from extensions import db


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)   # 해시만 저장(평문 금지)
  role = db.Column(db.Integer, nullable=False, default=ROLE_GENERAL)  # 0=일반 1=골드 2=관리자
  created_at = db.Column(db.DateTime, default=datetime.now)

  def to_dict(self):
    return {
        'id': self.id,
        'username': self.username,
        'role': self.role,
        'role_name': ROLE_NAMES.get(self.role, '알 수 없음'),
        'created_at': self.created_at.isoformat() if self.created_at else None,
    }

  def __repr__(self):
    return f'<User {self.username} role={self.role}>'
