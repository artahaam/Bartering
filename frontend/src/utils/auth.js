export function saveToken(token) {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('token', token);
  }
}

export function getToken() {
  if (typeof localStorage !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
}

export function logout() {
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem('token');
    window.location.href = '/login'; // redirect on logout
  }
}

export function isLoggedIn() {
  if (typeof localStorage === 'undefined') return false;
  return !!localStorage.getItem('token');
}