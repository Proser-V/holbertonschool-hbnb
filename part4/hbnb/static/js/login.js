document.getElementById('login-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
    const response = await fetch('/api/v1/users/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      document.getElementById('error-message').textContent = data.error || 'Erreur de connexion.';
      return;
    }

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);

    window.location.href = "/";
  } catch (err) {
  console.error('Erreur réseau ou parsing JSON:', err);
  document.getElementById('error-message').textContent = 'Erreur serveur.';
}
});