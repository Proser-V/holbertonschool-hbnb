import { apiFetch } from './refresh_token.js';

function expandRanges(ranges) {
  const lockedDates = [];
  ranges.forEach(range => {
    const start = new Date(range.start_date);
    const end = new Date(range.end_date);
    let current = new Date(start);
    while (current <= end) {
      lockedDates.push(current.toISOString().slice(0, 10));
      current.setDate(current.getDate() + 1);
    }
  });
  return lockedDates;
}

const picker = new Litepicker({
  element: document.getElementById('calendar'),
  inlineMode: true,
  singleMode: false,
  format: 'YYYY-MM-DD',
  numberOfMonths: 2,
  numberOfColumns: 2,
  disallowLockDaysInRange: true,
  lockDays: expandRanges(reservedRanges),
  setup: (picker) => {
    picker.on('selected', (start, end) => {
      if (start && end) {
        document.getElementById('selected-dates').textContent =
          `Du ${start.format('DD/MM/YYYY')} au ${end.format('DD/MM/YYYY')}`;
      }
    });
  }
});

document.getElementById('btn-book').addEventListener('click', async function () {
  const startDate = picker.getStartDate();
  const endDate = picker.getEndDate();

  if (!startDate || !endDate) {
    alert("Veuillez sélectionner une plage de dates avant de réserver.");
    return;
  }

  const place_id = document.getElementById('calendar').dataset.placeId

  try {
    const res = await apiFetch(`/api/v1/bookings/${place_id}`, {
      method: 'POST',
      body: JSON.stringify({
        start_date: startDate.format('YYYY-MM-DD'),
        end_date: endDate.format('YYYY-MM-DD')
      })
    });

    if (res.ok) {
      alert('Réservation enregistrée avec succès !');
      window.location.href = `/place/${place_id}`;
    } else {
      const error = await res.json();
      alert(`Erreur : ${error.message || 'Impossible de réserver'}`);
    }
  } catch (err) {
    console.error(err);
    alert("Erreur réseau");
  }
});