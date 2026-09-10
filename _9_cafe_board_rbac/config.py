"""설정 한 곳에 모으기.

이 실습의 목적은 "접근 제어(RBAC)" 그 자체이므로, MySQL 같은 별도 DB 설치 없이
바로 실행되도록 기본값을 SQLite 파일로 둔다. 필요하면 .env 의 DATABASE_URL 로
MySQL 등 다른 DB로 바꿀 수 있다(_7_board_test 와 동일한 방식).
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///cafe.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-only-change-me')
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
