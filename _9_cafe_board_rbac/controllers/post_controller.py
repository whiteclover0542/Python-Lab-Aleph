"""카페이야기 전체 게시판 — 로그인만 하면 등급 무관 누구나 글쓰기 가능.

등급별 페이지(/api/gold, /api/admin)와 대조되는 기준선: 여기는 role 체크가 없다.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from extensions import db
from models import Post

post_bp = Blueprint('post', __name__, url_prefix='/api/posts')


@post_bp.route('', methods=['GET'])
def get_posts():
  posts = Post.query.order_by(Post.id.desc()).limit(50).all()
  return jsonify({'posts': [p.to_dict() for p in posts]})


@post_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
  user_id = int(get_jwt_identity())
  data = request.get_json(silent=True) or {}
  if not data.get('title') or not data.get('content'):
    return jsonify({'msg': 'title, content 는 필수입니다.'}), 400

  post = Post(title=data['title'], content=data['content'], author_id=user_id)
  db.session.add(post)
  db.session.commit()
  return jsonify({'msg': '게시글이 등록되었습니다.', 'id': post.id}), 201


@post_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
  user_id = int(get_jwt_identity())
  post = db.get_or_404(Post, id)
  if post.author_id != user_id:
    return jsonify({'msg': '권한이 없습니다.'}), 403

  data = request.get_json(silent=True) or {}
  post.title = data.get('title', post.title)
  post.content = data.get('content', post.content)
  db.session.commit()
  return jsonify({'msg': '수정되었습니다.'})


@post_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
  user_id = int(get_jwt_identity())
  post = db.get_or_404(Post, id)
  if post.author_id != user_id:
    return jsonify({'msg': '권한이 없습니다.'}), 403

  db.session.delete(post)
  db.session.commit()
  return jsonify({'msg': '삭제되었습니다.'})
