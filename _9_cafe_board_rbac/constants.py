"""등급(권한) 상수.

숫자가 클수록 상위 등급이다. role_required(min_role) 는 "min_role 이상"을 의미한다.
  일반등급(0) : 최초 가입 시 기본값 — 누구나 이 등급으로 시작한다.
  골드등급(1) : 중간 관리자 — 관리자가 승급시켜야 한다.
  관리자  (2) : 회원 등급을 조회/수정/삭제할 수 있다.
"""
ROLE_GENERAL = 0
ROLE_GOLD = 1
ROLE_ADMIN = 2

ROLE_NAMES = {
    ROLE_GENERAL: '일반등급',
    ROLE_GOLD: '골드등급',
    ROLE_ADMIN: '관리자',
}
