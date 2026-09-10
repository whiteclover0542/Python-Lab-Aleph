/* Aegis Access Lab 공통 인증/등급 유틸리티 — 모든 페이지가 이 파일 하나만 불러오면 된다.
 * 로그인 모달(partials/_auth_modal.html)과 헤더(partials/_nav.html)가 이 파일의
 * 함수/ID 이름에 맞춰져 있으므로, 새 페이지를 만들 때도 그대로 include 하면 된다.
 */
const Site = (() => {
  let isLoginMode = true;
  let onAuthSuccess = null; // 로그인 성공 후 호출할 페이지별 콜백

  const ROLE_NAMES = ['옵저버', '가디언', '센티널'];
  const ROLE_BADGE = [
    'bg-gray-100 text-gray-600',
    'bg-amber-100 text-amber-700',
    'bg-rose-100 text-rose-700',
  ];

  function getToken() {
    return localStorage.getItem('token');
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>'"]/g,
      c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[c] || c));
  }

  async function fetchMe() {
    const token = getToken();
    if (!token) return null;
    try {
      const res = await fetch('/api/auth/me', { headers: { Authorization: `Bearer ${token}` } });
      if (!res.ok) return null;
      return await res.json();
    } catch (e) {
      return null;
    }
  }

  function renderNav(me) {
    const html = me
      ? `<span class="text-sm text-gray-700 whitespace-nowrap">로그인: <strong>${escapeHtml(me.username)}</strong></span>
         <span class="text-xs font-bold px-2 py-1 rounded-full ${ROLE_BADGE[me.role]} whitespace-nowrap"
               title="DB에서 매 요청마다 확인한 최신 권한">권한: ${escapeHtml(me.role_name)}</span>
         <button onclick="Site.logout()" class="text-sm text-red-500 hover:underline">로그아웃</button>`
      : `<button onclick="Site.openAuthModal(true)" class="text-sm text-amber-700 font-medium hover:underline">로그인</button>
         <button onclick="Site.openAuthModal(false)" class="bg-amber-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-amber-700 transition">회원가입</button>`;
    ['auth-nav', 'auth-nav-mobile'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.innerHTML = html;
    });
  }

  /** 예외(접근 거부) 화면 — 요구사항 6번: 등급이 맞지 않으면 이 카드를 보여준다. */
  function forbiddenHtml(reason, requiredRole, currentRole) {
    return `
      <div class="bg-white border border-rose-200 rounded-xl shadow-sm p-10 text-center">
        <div class="text-5xl mb-4">⛔</div>
        <h2 class="text-xl font-bold text-rose-600 mb-2">접근 권한이 없습니다</h2>
        <p class="text-gray-500 mb-1">${escapeHtml(reason || '')}</p>
        <p class="text-sm text-gray-400">
          필요 등급: <strong>${ROLE_NAMES[requiredRole]}</strong>
          ${currentRole !== null && currentRole !== undefined
            ? ` / 현재 등급: <strong>${ROLE_NAMES[currentRole]}</strong>` : ''}
        </p>
        <a href="/" class="inline-block mt-6 text-sm text-amber-700 hover:underline">← 게시판으로 돌아가기</a>
      </div>`;
  }

  /**
   * 페이지 진입 가드.
   *   requiredRole == null  → 등급 무관(공개 페이지). 로그인 상태만 onAllowed 로 넘겨준다.
   *   requiredRole == 0/1/2 → 해당 등급 미만이면 containerId 자리에 예외화면을 그리고 끝낸다.
   */
  async function guardPage(requiredRole, containerId, onAllowed) {
    const me = await fetchMe();
    renderNav(me);

    if (requiredRole === null || requiredRole === undefined) {
      if (onAllowed) await onAllowed(me);
      return;
    }

    const container = document.getElementById(containerId);
    if (!me) {
      container.innerHTML = forbiddenHtml('로그인이 필요합니다.', requiredRole, null);
      return;
    }
    if (me.role < requiredRole) {
      container.innerHTML = forbiddenHtml('등급이 부족합니다.', requiredRole, me.role);
      return;
    }
    if (onAllowed) await onAllowed(me);
  }

  function openAuthModal(loginMode, afterSuccess) {
    isLoginMode = loginMode;
    onAuthSuccess = afterSuccess || null;
    document.getElementById('modal-title').innerText = loginMode ? '로그인' : '회원가입';
    document.getElementById('modal-submit-btn').innerText = loginMode ? '로그인' : '가입하기';
    document.getElementById('modal-username').value = '';
    document.getElementById('modal-password').value = '';
    document.getElementById('auth-modal').classList.remove('hidden');
  }

  function closeAuthModal() {
    document.getElementById('auth-modal').classList.add('hidden');
  }

  async function submitAuth() {
    const username = document.getElementById('modal-username').value.trim();
    const password = document.getElementById('modal-password').value;
    if (!username || !password) { alert('아이디/비밀번호를 입력하세요.'); return; }

    const endpoint = isLoginMode ? '/api/auth/login' : '/api/auth/register';
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();

    if (!res.ok) { alert(data.msg || '오류가 발생했습니다.'); return; }

    if (isLoginMode) {
      localStorage.setItem('token', data.access_token);
      closeAuthModal();
      const me = await fetchMe();
      renderNav(me);
      if (onAuthSuccess) onAuthSuccess(me);
      else location.reload();
    } else {
      alert('회원가입 완료! (옵저버 등급으로 가입되었습니다) 로그인해주세요.');
      openAuthModal(true, onAuthSuccess);
    }
  }

  function logout() {
    localStorage.removeItem('token');
    location.href = '/';
  }

  return {
    getToken, fetchMe, renderNav, guardPage, forbiddenHtml, escapeHtml,
    openAuthModal, closeAuthModal, submitAuth, logout,
  };
})();
