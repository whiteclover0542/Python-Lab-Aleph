# 카페이야기 RBAC 연습

회원 등급을 `일반(0)`, `골드(1)`, `관리자(2)`로 나누어 화면과 API 양쪽에서
접근 제어를 확인하는 Flask 연습 프로젝트입니다.

## 실행

```powershell
cd _9_cafe_board_rbac
python -m pip install -r requirements.txt
python -m flask --app app create-admin admin
python app.py
```

`http://localhost:5000`에서 확인합니다. `create-admin` 명령은 최초 관리자용이며
비밀번호를 화면에 표시하지 않고 두 번 입력받습니다. 일반 회원가입 요청에 `role`을
넣어도 서버가 무시하고 항상 일반등급(0)으로 생성합니다.

## 확인 시나리오

1. 일반 회원을 가입하고 로그인합니다.
2. `/gold`, `/admin`에서 접근 거부 화면이 표시되는지 확인합니다.
3. 관리자 계정으로 `/admin`에 들어가 일반 회원을 골드로 변경합니다.
4. 해당 회원은 재로그인 없이 `/gold`에 접근할 수 있지만 `/admin`에는 접근할 수 없습니다.
5. 관리자는 회원 목록 조회, 등급 변경, 삭제가 가능합니다.

브라우저의 등급 검사는 안내 화면을 위한 것이며, 실제 보안은
`/api/gold/*`, `/api/admin/*`의 서버 측 `role_required()`가 담당합니다.

## 테스트

```powershell
python -m pytest -q
```
