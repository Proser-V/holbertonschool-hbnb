// Main API fetch wrapper with automatic token refresh on 401 errors
export async function apiFetch(url, options = {}, retry = true) {
    // Perform the initial fetch request
    const res = await fetch(url, {
        ...options, // Spread all user-provided options (like "method")
        headers: {
            ...(options.headers || {}), // Preserve any custom headers
            'Content-Type': 'application/json' // Add in headers: always send JSON
        },
        credentials: 'include' // Include cookies
    });

    // If the server responds with 401 (Unauthorized) and retry is allowed
    if (res.status === 401 && retry) {
        console.warn("Token expiré ou invalide, tentative de refresh...");

        // Try refreshing the token
        const refreshed = await tryRefreshToken();
        if (refreshed) {
            console.log("Refresh réussi, nouvelle tentative de", url);
            // Retry original request once after successful refresh
            return await apiFetch(url, options, false);
        } else {
            // If refresh failed, redirect user to login
            console.error("Échec du refresh, redirection vers /login");
            window.location.href = "/login";
            // Return dummy response with 401 to satisfy return contract
            return new Response(null, { status: 401 });
        }
    }

    // Return the original response (even if not OK)
    return res;
}

// Attempt to refresh the JWT token
async function tryRefreshToken() {
    try {
        // Send a POST request to the refresh endpoint
        const res = await fetch('/api/v1/users/refresh', {
            method: 'POST',
            credentials: 'include' // Include cookies for refresh
        });
        // Log status and return true if refresh was successful (status 200)
        console.log("Tentative de refresh, statut:", res.status);
        console.log("Réponse brute du refresh :", await res.text());
        return res.ok;
    } catch (err) {
        // Catch and log any network error
        console.error("Erreur lors du refresh:", err);
        return false;
    }
}

// Format a Pydantic validation error response into a user-friendly string.
export function formatPydanticError(errorData) {
    // Check if the response contains a list of validation errors
    if (errorData?.error && Array.isArray(errorData.error)) {
        return errorData.error.map(e => {
            // Build a readable field name from the location path
            const field = e.loc?.join('.') || 'champ inconnu'; // Join the location array into a dotted path like "body.field"
            const msg = e.msg || 'Erreur inconnue'; // Use default message if msg is missing
            return `${field} : ${msg}`;
        }).join('\n'); // Combine all error lines into one string separated by newlines
    }
    return errorData?.error || 'Erreur inconnue';
}
