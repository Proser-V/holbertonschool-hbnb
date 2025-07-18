document.addEventListener('DOMContentLoaded', () => {
    const userNav = document.getElementById('user-nav');
    const accessToken = localStorage.getItem('access_token');

    if (accessToken && userNav) {
        try {
            const decoded = jwt_decode(accessToken);
            const userId = decoded.sub || decoded.identity;
            console.log("Token décodé, userId:", userId);

            fetch(`/api/v1/users/${userId}`, {
            headers: { 'Authorization': `Bearer ${accessToken}` }
            })
            .then(res => {
            console.log("Réponse reçue du backend:", res.status);
            if (!res.ok) throw new Error('Erreur HTTP ' + res.status);
            return res.json();
            })
            .then(data => {
            console.log('Données utilisateur reçues:', data);

            userNav.innerHTML = `
                <a class="header-logout" href="#" id="logout-link">Logout</a>
                <a href="/profile/${userId}" id="user-profile-link">
                <img src="${data.photo_url || 'https://cdn0.iconfinder.com/data/icons/mobile-basic-vol-1/32/Profile-256.png'}" alt="Profil de ${data.first_name}" class="header-user-photo" />
                </a>
            `;

            document.getElementById('logout-link').onclick = e => {
                e.preventDefault();
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.reload();
            };
            })
            .catch(err => {
            console.warn('Erreur dans le .catch() de jwt.js:', err);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.reload();
            });
        } catch (err) {
            console.error("Erreur dans le bloc try/catch:", err);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        }
    }
});