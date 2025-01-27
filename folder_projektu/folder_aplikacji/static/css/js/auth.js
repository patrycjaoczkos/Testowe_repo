async function register() {
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message); // Sukces
            window.location.href = '/panel/'; // Przekierowanie do panelu użytkownika
        } else {
            alert(result.error || "Błąd rejestracji.");
        }
    } catch (error) {
        console.error("Błąd:", error);
        alert("Coś poszło nie tak. Spróbuj ponownie.");
    }
}
<div id="registerModal" class="modal">
    <div class="modal-content">
        <button class="close" onclick="closeModal('registerModal')">&times;</button>
        <h2>Rejestracja</h2>
        <input type="text" id="registerUsername" placeholder="Nazwa użytkownika" required>
        <input type="email" id="registerEmail" placeholder="Email" required>
        <input type="password" id="registerPassword" placeholder="Hasło" required>
        <button onclick="register()">Zarejestruj</button>
    </div>
</div>