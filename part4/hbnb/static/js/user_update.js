import { apiFetch } from './refresh_token.js';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('user-update-container');
  const button = document.getElementById('button-to-update-user');
  const cancelBtn = document.getElementById('cancel-update-form');
  const form = document.getElementById('user-update-form');

  button.addEventListener('click', () => {
    container.classList.add('expanding');
    setTimeout(() => {
      container.classList.add('show-form');
    }, 400);
  });

  cancelBtn.addEventListener('click', () => {
    container.classList.remove('show-form');
    setTimeout(() => {
      container.classList.remove('expanding');
    }, 400);
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userId = form.dataset.userId;

    const data = {
      first_name: form.first_name.value.trim() || undefined,
      last_name: form.last_name.value.trim() || undefined,
      email: form.email.value.trim() || undefined,
      password: form.password.value.trim() || undefined,
      photo_url: form.photo_url.value.trim() || undefined,
    };

    try {
      const response = await apiFetch(`/api/v1/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(data)
      });

      if (response.ok) {
        alert('Profil mis à jour !');
        location.reload();
      } else {
        const error = await response.json();
        alert(`Erreur : ${error.message || 'Impossible de mettre à jour le profil'}`);
      }
    } catch (err) {
      console.error(err);
      alert('Erreur réseau ou serveur');
    }
  });
});
