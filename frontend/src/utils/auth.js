const TokenKey = 'py-SEP-Token'

export function getToken() {
    return localStorage.getItem(TokenKey);
  }
  
  export function setToken(token) {
    console.log('infunction');
    localStorage.setItem(TokenKey, token);
  }
  
  export function removeToken() {
    localStorage.removeItem(TokenKey);
  }