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
    console.warn("🔒 Token expiré ou invalide, tentative de refresh...");

    const refreshed = await tryRefreshToken();
    if (refreshed) {
      console.log("Refresh réussi, nouvelle tentative de", url);
      return await apiFetch(url, options, false);
    } else {
      console.error("Échec du refresh, redirection vers /login");
      window.location.href = "/login";
      return new Response(null, { status: 401 });
    }
  }

  return res;
}

async function tryRefreshToken() {
  try {
    const res = await fetch('/api/v1/users/refresh', {
      method: 'POST',
      credentials: 'include'
    });
    console.log("Tentative de refresh, statut:", res.status);
    return res.ok;
  } catch (err) {
    console.error("Erreur lors du refresh:", err);
    return false;
  }
}