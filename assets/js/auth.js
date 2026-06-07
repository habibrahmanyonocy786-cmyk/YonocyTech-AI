const USERS_KEY = 'yonocytech_users';
const SESSION_KEY = 'yonocytech_session';

function getUsers() {
  return JSON.parse(localStorage.getItem(USERS_KEY) || '[]');
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

function getSession() {
  return JSON.parse(localStorage.getItem(SESSION_KEY) || 'null');
}

function saveSession(user) {
  localStorage.setItem(SESSION_KEY, JSON.stringify({
    email: user.email,
    name: user.name,
    role: user.role || 'user',
    loggedIn: Date.now()
  }));
}

function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}

function isLoggedIn() {
  const session = getSession();
  return session && session.email;
}

function isAdmin() {
  const session = getSession();
  return session && session.role === 'admin';
}

function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = 'login.html';
    return false;
  }
  return true;
}

function requireAdmin() {
  if (!isAdmin()) {
    window.location.href = 'dashboard.html';
    return false;
  }
  return true;
}

function logout() {
  clearSession();
  window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const loginError = document.getElementById('loginError');
  const registerError = document.getElementById('registerError');
  const registerSuccess = document.getElementById('registerSuccess');

  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      loginError.style.display = 'none';
      const email = document.getElementById('loginEmail').value.trim();
      const password = document.getElementById('loginPassword').value;
      const users = getUsers();
      const user = users.find(u => u.email === email && u.password === password);
      if (user) {
        saveSession(user);
        window.location.href = user.role === 'admin' ? 'admin.html' : 'dashboard.html';
      } else {
        loginError.textContent = '❌ Invalid email or password. Please try again.';
        loginError.style.display = 'block';
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
      e.preventDefault();
      registerError.style.display = 'none';
      registerSuccess.style.display = 'none';
      const name = document.getElementById('regName').value.trim();
      const email = document.getElementById('regEmail').value.trim();
      const password = document.getElementById('regPassword').value;
      const confirm = document.getElementById('regConfirm').value;
      if (password !== confirm) {
        registerError.textContent = '❌ Passwords do not match.';
        registerError.style.display = 'block';
        return;
      }
      const users = getUsers();
      if (users.find(u => u.email === email)) {
        registerError.textContent = '❌ An account with this email already exists.';
        registerError.style.display = 'block';
        return;
      }
      const isFirst = users.length === 0;
      const newUser = {
        name,
        email,
        password,
        role: isFirst ? 'admin' : 'user',
        plan: 'free',
        createdAt: new Date().toISOString(),
        lastLogin: null
      };
      users.push(newUser);
      saveUsers(users);
      registerSuccess.textContent = isFirst
        ? '✅ Admin account created! You are the first user — automatically set as admin. Redirecting...'
        : '✅ Account created successfully! Redirecting to dashboard...';
      registerSuccess.style.display = 'block';
      saveSession(newUser);
      setTimeout(() => {
        window.location.href = isFirst ? 'admin.html' : 'dashboard.html';
      }, 1500);
    });
  }

  if (window.location.hash === '#register') {
    const tab = document.querySelector('[data-tab="auth-register"]');
    if (tab) tab.click();
  }
});

function socialLogin(provider) {
  const loginError = document.getElementById('loginError');
  if (loginError) {
    loginError.textContent = `🌐 ${provider} login coming soon. Use email/password for now.`;
    loginError.style.display = 'block';
  }
}
