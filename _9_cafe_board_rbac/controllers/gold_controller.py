"""가디언 전용 룸 — role_required(ROLE_GOLD) 로 막혀 있다.

옵저버(0)가 호출하면 403, 가디언(1)/센티널(2)은 통과한다.
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from constants import ROLE_GOLD
from decorators import role_required
from extensions import db
from models import User

gold_bp = Blueprint('gold', __name__, url_prefix='/api/gold')


@gold_bp.route('/lounge', methods=['GET'])
@role_required(ROLE_GOLD)
def lounge():
  user = db.session.get(User, int(get_jwt_identity()))
  return jsonify({
      'msg': f'{user.username}님, 가디언 룸에 오신 것을 환영합니다.',
      'benefits': ['보안 공지 열람', '가디언 검증 실습', '접근 기록 확인'],
  })
