"""등급(권한) 상수.

숫자가 클수록 상위 등급이다. role_required(min_role) 는 "min_role 이상"을 의미한다.
  옵저버(0)  : 최초 가입 시 기본값 — 누구나 이 등급으로 시작한다.
  가디언(1)  : 중간 운영 권한 — 센티널이 승급시킨다.
  센티널(2)  : 회원 정보를 조회/수정/삭제할 수 있다.
"""
ROLE_GENERAL = 0
ROLE_GOLD = 1
ROLE_ADMIN = 2

ROLE_NAMES = {
    ROLE_GENERAL: '옵저버',
    ROLE_GOLD: '가디언',
    ROLE_ADMIN: '센티널',
}
