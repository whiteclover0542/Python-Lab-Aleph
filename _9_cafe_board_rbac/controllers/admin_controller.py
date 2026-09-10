"""센티널 콘솔 API — 회원 목록 조회 / 등급 수정 / 삭제.

role_required(ROLE_ADMIN) 으로 막혀 있어 센티널(2)만 통과한다.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity

from constants import ROLE_ADMIN, ROLE_NAMES
from decorators import role_required
from extensions import db
from models import User

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/users', methods=['GET'])
@role_required(ROLE_ADMIN)
def list_users():
  users = User.query.order_by(User.id).all()
  return jsonify({'users': [u.to_dict() for u in users]})


@admin_bp.route('/users/<int:id>', methods=['PUT'])
@role_required(ROLE_ADMIN)
def update_user(id):
  data = request.get_json(silent=True) or {}
  role = data.get('role')
  username = (data.get('username') or '').strip()

  if not username:
    return jsonify({'msg': 'username은 비워둘 수 없습니다.'}), 400
  # bool은 Python에서 int의 하위 타입이므로 True(1), False(0)를 따로 거부한다.
  if isinstance(role, bool):
    return jsonify({'msg': f'role 은 {sorted(ROLE_NAMES)} 중 하나여야 합니다.'}), 400
  if role not in ROLE_NAMES:
    return jsonify({'msg': f'role 은 {sorted(ROLE_NAMES)} 중 하나여야 합니다.'}), 400

  user = db.get_or_404(User, id)
  duplicate = User.query.filter(User.username == username, User.id != id).first()
  if duplicate:
    return jsonify({'msg': '이미 존재하는 사용자입니다.'}), 400

  current_id = int(get_jwt_identity())
  if id == current_id and role != ROLE_ADMIN:
    return jsonify({'msg': '현재 로그인한 센티널 본인의 등급은 낮출 수 없습니다.'}), 400
  user.username = username
  user.role = role
  db.session.commit()
  return jsonify({'msg': '등급이 변경되었습니다.', **user.to_dict()})


@admin_bp.route('/users/<int:id>', methods=['DELETE'])
@role_required(ROLE_ADMIN)
def delete_user(id):
  current_id = int(get_jwt_identity())
  if id == current_id:
    return jsonify({'msg': '본인 계정은 삭제할 수 없습니다.'}), 400

  user = db.get_or_404(User, id)
  db.session.delete(user)
  db.session.commit()
  return jsonify({'msg': '삭제되었습니다.'})
