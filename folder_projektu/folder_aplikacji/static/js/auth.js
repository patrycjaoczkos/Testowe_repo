// Funkcja do obsługi rejestracji użytkownika
async function register() {
    // Pobieranie danych z formularza
    const username = document.getElementById('registerUsername').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value.trim();

    // Sprawdzanie, czy wszystkie pola zostały wypełnione
    if (!username || !email || !password) {
        alert("Wszystkie pola muszą być wypełnione.");
        return;
    }

    // Pobieranie tokenu CSRF z HTML
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        // Wysyłanie danych do endpointu rejestracji
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken, // Dodanie tokenu CSRF do nagłówków
            },
            body: JSON.stringify({ username, email, password }), // Dane w formacie JSON
        });

        const result = await response.json(); // Parsowanie odpowiedzi z serwera

        if (response.ok) {
            // Sukces rejestracji
            alert(result.message || "Rejestracja zakończona sukcesem!");
            window.location.href = '/panel/'; // Przekierowanie do panelu użytkownika
        } else {
            // Błąd rejestracji
            alert(result.error || "Rejestracja nie powiodła się.");
            console.error("Błąd serwera:", result);
        }
    } catch (error) {
        // Obsługa błędów połączenia
        console.error("Błąd połączenia:", error);
        alert("Nie udało się połączyć z serwerem. Spróbuj ponownie później.");
    }
}

// Funkcja do obsługi logowania użytkownika
async function login() {
    // Pobieranie danych z formularza
    const username = document.getElementById('loginUsername').value.trim();
    const password = document.getElementById('loginPassword').value.trim();

    // Sprawdzanie, czy wszystkie pola zostały wypełnione
    if (!username || !password) {
        alert("Wszystkie pola muszą być wypełnione.");
        return;
    }

    // Pobieranie tokenu CSRF z HTML
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    try {
        // Wysyłanie danych do endpointu logowania
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken, // Dodanie tokenu CSRF do nagłówków
            },
            body: JSON.stringify({ username, password }), // Dane w formacie JSON
        });

        const result = await response.json(); // Parsowanie odpowiedzi z serwera

        if (response.ok) {
            // Sukces logowania
            alert(result.message || "Zalogowano pomyślnie!");
            window.location.href = '/panel/'; // Przekierowanie do panelu użytkownika
        } else {
            // Błąd logowania
            alert(result.error || "Logowanie nie powiodło się.");
            console.error("Błąd serwera:", result);
        }
    } catch (error) {
        // Obsługa błędów połączenia
        console.error("Błąd połączenia:", error);
        alert("Nie udało się połączyć z serwerem. Spróbuj ponownie później.");
    }
}

