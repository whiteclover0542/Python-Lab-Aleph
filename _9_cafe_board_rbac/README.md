# Aegis Access Lab RBAC 연습

회원 등급을 `옵저버(0)`, `가디언(1)`, `센티널(2)`로 나누어 화면과 API 양쪽에서
접근 제어를 확인하는 Flask 연습 프로젝트입니다.

## 실행

```powershell
cd _9_cafe_board_rbac
python -m pip install -r requirements.txt
python -m flask --app app create-admin admin
python app.py
```

`http://localhost:5000`에서 확인합니다. `create-admin` 명령은 최초 센티널용이며
비밀번호를 화면에 표시하지 않고 두 번 입력받습니다. 일반 회원가입 요청에 `role`을
넣어도 서버가 무시하고 항상 옵저버(0)로 생성합니다.

## 확인 시나리오

1. 일반 회원을 가입하고 로그인합니다.
2. `/gold`, `/admin`에서 접근 거부 화면이 표시되는지 확인합니다.
3. 센티널 계정으로 `/admin`에 들어가 옵저버를 가디언으로 변경합니다.
4. 해당 회원은 재로그인 없이 `/gold`에 접근할 수 있지만 `/admin`에는 접근할 수 없습니다.
5. 센티널은 회원 목록 조회, 아이디·등급 변경, 삭제가 가능합니다.

제출 화면에서는 로그인 후 헤더에 표시되는 `로그인: 사용자명`, `권한: 등급명`을
확인합니다. 권한은 `/api/auth/me`이 DB에서 매 요청마다 읽어온 최신값입니다.
가디언 룸과 센티널 콘솔은 접근 허용 상태를, 등급 미달 화면은 접근 거부·필요 권한·현재
권한을 표시합니다.

브라우저의 등급 검사는 안내 화면을 위한 것이며, 실제 보안은
`/api/gold/*`, `/api/admin/*`의 서버 측 `role_required()`가 담당합니다.

## 테스트

```powershell
python -m pytest -q
```
