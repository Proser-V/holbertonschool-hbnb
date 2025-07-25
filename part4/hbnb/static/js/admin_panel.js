document.getElementById('open-admin-panel-user').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-user');
    });

document.getElementById('open-admin-panel-place').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-place');
    });

document.getElementById('open-admin-panel-review').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-review');
    });

document.getElementById('open-admin-panel-booking').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-booking');
    });

document.getElementById('open-admin-panel-amenity').addEventListener('click', () => {
    const panel = document.getElementById('admin-panel');
    panel.classList.toggle('expanding-amenity');
    });