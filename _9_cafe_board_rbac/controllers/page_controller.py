"""화면(HTML) 라우트. 여기서는 등급 검사를 하지 않는다.

로그인 토큰이 서버 세션이 아니라 브라우저 localStorage 에 있는 방식(Bearer 토큰)이라,
서버는 페이지 GET 요청만으로는 누가 요청했는지 알 수 없다. 그래서 실제 접근 제어는
2단계로 나뉜다.
  1) 화면(JS)  : /api/auth/me 로 현재 등급을 물어보고, 등급 미달이면 예외화면을 그린다.
  2) API(서버) : /api/gold/*, /api/admin/* 가 role_required() 로 다시 한 번 막는다.
1번은 사용자 경험(UX)일 뿐이고, 2번이 실제 방어선이다 — devtools 로 1번을 무시하고
API 를 직접 호출해도 2번에서 403 이 떨어지는지가 이 실습의 핵심 확인 포인트다.
"""
from flask import Blueprint, render_template

page_bp = Blueprint('page', __name__)


@page_bp.route('/')
def index():
  return render_template('index.html')


@page_bp.route('/gold')
def gold_page():
  return render_template('gold.html')


@page_bp.route('/admin')
def admin_page():
  return render_template('admin.html')
