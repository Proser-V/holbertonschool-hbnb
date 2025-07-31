import { apiFetch, formatPydanticError } from './refresh_token.js';

// Helper function to expand reserved date ranges into individual date strings
function expandRanges(ranges) {
    const lockedDates = []; // Array to store all individual locked dates
    ranges.forEach(range => {
        const start = new Date(range.start_date); // Parse start date
        const end = new Date(range.end_date); // Parse end date
        let current = new Date(start); // Initialize a date cursor
        while (current <= end) {
            // Push date in 'YYYY-MM-DD' format
            lockedDates.push(current.toISOString().slice(0, 10));
            // Move to next day
            current.setDate(current.getDate() + 1);
        }
    });
    return lockedDates; // Return list of locked dates
}

// Initialize Litepicker calendar
const picker = new Litepicker({
    element: document.getElementById('calendar'), // Attach to element with id 'calendar
    inlineMode: true, // Display the calendar directly in the page (not a popup)
    singleMode: false, // Allow selecting a date range
    format: 'YYYY-MM-DD', // Format used internally
    numberOfMonths: 2, // Display 2 months at a time
    numberOfColumns: 2, // Arrange months in 2 columns
    disallowLockDaysInRange: true, // Prevent range selection overlapping locked dates
    lockDays: expandRanges(reservedRanges), // Provide locked (unavailable) days
    setup: (picker) => {
        // Event handler when user selects a date range
        picker.on('selected', (start, end) => {
            if (start && end) {
                // Display selected dates in text format
                document.getElementById('selected-dates').textContent =
                `Du ${start.format('DD/MM/YYYY')} au ${end.format('DD/MM/YYYY')}`;
            }
        });
    }
});

// Handle booking button click
document.getElementById('btn-book').addEventListener('click', async function (e) {
    e.preventDefault();

    const startDate = picker.getStartDate(); // Get selected start date
    const endDate = picker.getEndDate(); // Get selected end date

    if (!startDate || !endDate) { // Validate that both dates are selected
        alert("Veuillez sélectionner une plage de dates avant de réserver.");
        return;
    }

    if (startDate.isSame(endDate, 'day')) {
        alert("Veuillez sélectionner au moins une nuit (2 dates consécutives).");
        return;
    }

    // Retrieve place ID from the dataset
    const place_id = document.getElementById('calendar').dataset.placeId

    try {
        // Send booking request to API
        const res = await apiFetch(`/api/v1/bookings/${place_id}`, {
            method: 'POST',
            body: JSON.stringify({
                start_date: startDate.format('YYYY-MM-DD'),
                end_date: endDate.format('YYYY-MM-DD')
            })
        });

        // On success, notify and redirect
        if (res.ok) {
            alert('Réservation enregistrée avec succès !');
            window.location.href = `/place/${place_id}`;
        } else {
            // Attempt to parse the JSON error response
            const errorData = await res.json();
            // Format Pydantic-style validation errors into a user-friendly message
            const prettyMessage = formatPydanticError(errorData);
            // Display the formatted error to the user
            alert(`Erreur :\n${prettyMessage}`);
        }
    } catch (err) {
        // Catch network or unexpected errors
        console.error(err);
        alert("Erreur réseau");
    }
});
