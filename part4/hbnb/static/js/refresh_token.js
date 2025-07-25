export async function apiFetch(url, options = {}, retry = true) {
  const res = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  });

  if (res.status === 401 && retry) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      return apiFetch(url, options, false);
    } else {
      window.location.href = "/login";
    }
  }

  return res;
}

async function tryRefreshToken() {
  
  const res = await fetch('/refresh', {
    method: 'POST',
    credentials: 'include'
  });
  return res.ok;
}