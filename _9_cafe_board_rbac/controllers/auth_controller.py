"""회원가입 / 로그인 / 내 정보 조회.

핵심 규칙: 회원가입은 항상 일반등급(role=0)으로만 생성된다. 요청 바디에 role 을
몰래 끼워 보내도(예: {"role": 2}) 서버는 그 값을 절대 읽지 않는다 — 등급 상승은
오직 관리자 페이지(/api/admin/users)를 통해서만 가능해야 하기 때문이다.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from constants import ROLE_GENERAL
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json(silent=True) or {}
  username = (data.get('username') or '').strip()
  password = data.get('password') or ''
  if not username or not password:
    return jsonify({'msg': 'username, password 는 필수입니다.'}), 400
  if User.query.filter_by(username=username).first():
    return jsonify({'msg': '이미 존재하는 사용자입니다.'}), 400

  # 클라이언트가 role 을 보내더라도 무시하고 항상 일반등급으로 가입시킨다.
  user = User(username=username, password=generate_password_hash(password),
              role=ROLE_GENERAL)
  db.session.add(user)
  db.session.commit()
  return jsonify({'msg': '회원가입 성공 (일반등급으로 가입되었습니다.)'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json(silent=True) or {}
  user = User.query.filter_by(username=data.get('username')).first()
  if not user or not check_password_hash(user.password, data.get('password', '')):
    return jsonify({'msg': '아이디 또는 비밀번호가 잘못되었습니다.'}), 401

  token = create_access_token(identity=str(user.id))
  return jsonify(access_token=token, **user.to_dict())


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
  """토큰의 role 이 아니라 항상 DB 최신값을 반환한다.

  관리자가 방금 등급을 바꿨어도 이 엔드포인트를 통해 재로그인 없이 최신 등급을
  바로 확인할 수 있다 — 화면(헤더 배지, 골드/관리자 페이지 가드)이 이 응답으로 갱신된다.
  """
  user = db.session.get(User, int(get_jwt_identity()))
  if not user:
    return jsonify({'msg': '사용자를 찾을 수 없습니다.'}), 404
  return jsonify(user.to_dict())
