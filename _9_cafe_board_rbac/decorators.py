"""등급 기반 접근 제어 데코레이터.

JWT 안에 role 을 실어 보내는 방식도 가능하지만, 그러면 관리자가 등급을 바꿔도
클라이언트가 재로그인하기 전까지는 옛 토큰의 role 이 계속 통한다(권한 회수가
즉시 반영되지 않는 흔한 실수). 그래서 여기서는 토큰에서 user id 만 꺼내고,
role 은 매 요청마다 DB에서 새로 읽는다 — 승급/강등/삭제가 다음 요청부터 바로 먹힌다.
"""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from constants import ROLE_NAMES
from extensions import db
from models import User


def role_required(min_role):
  """이 등급 이상만 통과. 미로그인 401, 등급 미달 403."""
  def decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      verify_jwt_in_request()
      user = db.session.get(User, int(get_jwt_identity()))
      if not user:
        return jsonify({'msg': '사용자를 찾을 수 없습니다.'}), 401
      if user.role < min_role:
        return jsonify({
            'msg': f'접근 권한이 없습니다. ({ROLE_NAMES.get(min_role, "?")} 이상 필요)',
            'required_role': min_role,
            'required_role_name': ROLE_NAMES.get(min_role, '?'),
            'current_role': user.role,
            'current_role_name': ROLE_NAMES.get(user.role, '?'),
        }), 403
      return fn(*args, **kwargs)
    return wrapper
  return decorator
