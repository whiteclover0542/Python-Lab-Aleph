"""골드등급 전용 라운지 — role_required(ROLE_GOLD) 로 막혀 있다.

일반등급(0)이 호출하면 403, 골드(1)/관리자(2)는 통과한다.
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
      'msg': f'{user.username}님, 골드등급 라운지에 오신 것을 환영합니다.',
      'benefits': ['비공개 정모 공지', '골드 전용 이벤트 응모', '광고 제거'],
  })
