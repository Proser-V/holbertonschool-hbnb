function toDayOnly(dateStr) {
    const d = new Date(dateStr);
    return new Date(d.getFullYear(), d.getMonth(), d.getDate());
}

let disabledRanges = [];
try {
    const res = await fetch(`/api/v1/bookings/places/${placeId}/pending_booking`, {
        headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
    });
    if (res.ok) {
        const bookings = await res.json();
        disabeldRanges = bookings.map(b => ({
            from: toDayOnly(b.start_date),
            to: toDayOnly(b.end_date)
        }));
    } else {
        console.warn('Can\'t fetch existing bookings');
    }
} catch (err) {
    console.error('Error fetching bookings:', err);
}
let selectedStart = null;
let selectedEnd = null;
flatpickr("#date-range", {
    mode: "range",
    minDate: "today",
    dateFormat: "Y-m-d",
    disable: disabledRanges,
    inline: true,
    onChange: function (selectedDates) {
        if (selectedDates.length === 2) {
            selectedStart = selectedDates[0].toISOString();
            selectedEnd = selectedDates[1].toISOString();
            document.getElementById('book-button').style.display = 'inline-block';
        }
    },
    onReady: function (selectedDates, dateStr, instance) {
        instance.open();
    }
});
const body = { selectedStart, selectedEnd };
console.log(JSON.stringify(body));
const res = await fetch('/api/v1/users/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    credentials: 'include',
    body: JSON.stringify(body)
});