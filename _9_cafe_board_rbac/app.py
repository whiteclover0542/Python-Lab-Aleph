"""엔트리포인트 — 앱 팩토리(create_app) 패턴. (_7_board_test 와 동일한 구조)

구조
  config.py       설정(.env 로딩) — 기본은 SQLite 파일이라 별도 DB 설치 없이 바로 실행된다.
  extensions.py   db · jwt 인스턴스
  constants.py    등급 상수 (옵저버=0, 가디언=1, 센티널=2)
  decorators.py   role_required() — 등급 기반 접근 제어 데코레이터
  models/         User(role 포함) · Post
  controllers/    page · auth · post · gold · admin (블루프린트)
  templates/      화면 (partials/_nav.html = 공통 헤더: 가디언/센티널 링크 포함)

실행:  python app.py   →  http://localhost:5000
"""
import click
from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from controllers import all_blueprints
from extensions import db, jwt
from constants import ROLE_ADMIN
from models import User


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  # 확장 초기화
  db.init_app(app)
  jwt.init_app(app)

  # 컨트롤러(블루프린트) 등록
  for bp in all_blueprints:
    app.register_blueprint(bp)

  # 테이블 생성 (models 를 import 한 뒤여야 한다 — controllers 가 이미 import 함)
  with app.app_context():
    db.create_all()

  @app.cli.command('create-admin')
  @click.argument('username')
  @click.password_option(confirmation_prompt=True)
  def create_admin(username, password):
    """최초 관리자 계정을 안전하게 만든다 (예: flask create-admin admin)."""
    username = username.strip()
    if not username:
      raise click.ClickException('아이디는 비워둘 수 없습니다.')
    if not password:
      raise click.ClickException('비밀번호는 비워둘 수 없습니다.')
    if User.query.filter_by(username=username).first():
      raise click.ClickException('이미 존재하는 사용자입니다.')

    user = User(
        username=username,
        password=generate_password_hash(password),
        role=ROLE_ADMIN,
    )
    db.session.add(user)
    db.session.commit()
    click.echo(f'관리자 계정 "{username}"을 생성했습니다.')

  return app


app = create_app()


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
