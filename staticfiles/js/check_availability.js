document.addEventListener('DOMContentLoaded', function () {
    const usernameField = document.getElementById('username');
    const emailField = document.getElementById('email');
    const usernameMessage = document.getElementById('username-message');
    const emailMessage = document.getElementById('email-message');

    // Überprüfung des Benutzernamens
    usernameField.addEventListener('input', function () {
        const username = usernameField.value;

        if (username.length > 0) {
            fetch('/check-username/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ username: username })
            })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    usernameMessage.textContent = "Benutzername bereits vergeben";
                    usernameMessage.style.color = "red";
                } else {
                    usernameMessage.textContent = "Benutzername verfügbar";
                    usernameMessage.style.color = "green";
                }
            })
            .catch(error => {
                console.error("Fehler bei der Überprüfung des Benutzernamens:", error);
            });
        } else {
            usernameMessage.textContent = "";
        }
    });

    // Überprüfung der E-Mail
    emailField.addEventListener('input', function () {
        const email = emailField.value;

        if (email.length > 0) {
            fetch('/check-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    emailMessage.textContent = "E-Mail bereits vergeben";
                    emailMessage.style.color = "red";
                } else {
                    emailMessage.textContent = "E-Mail verfügbar";
                    emailMessage.style.color = "green";
                }
            })
            .catch(error => {
                console.error("Fehler bei der Überprüfung der E-Mail:", error);
            });
        } else {
            emailMessage.textContent = "";
        }
    });
});
