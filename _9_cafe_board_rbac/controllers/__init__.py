"""컨트롤러(블루프린트) 묶음. app.py 가 이 목록을 한 번에 등록한다."""
from .admin_controller import admin_bp
from .auth_controller import auth_bp
from .gold_controller import gold_bp
from .page_controller import page_bp
from .post_controller import post_bp

all_blueprints = (page_bp, auth_bp, post_bp, gold_bp, admin_bp)

__all__ = ['all_blueprints', 'page_bp', 'auth_bp', 'post_bp', 'gold_bp', 'admin_bp']
