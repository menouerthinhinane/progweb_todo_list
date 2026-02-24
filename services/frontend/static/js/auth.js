document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', login);
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', register);
    }
});

// Fonction de connexion
async function login(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');

    if (!username || !password) {
        showError(errorDiv, 'Veuillez remplir tous les champs');
        return;
    }

    try {
        const { ok, data } = await apiCall('/api/users/login', 'POST', { username, password });
        
        if (ok && data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('username', data.username);
            localStorage.setItem('userId', data.id);
            window.location.href = '/tasks';
        } else {
            showError(errorDiv, data.error || 'Identifiants incorrects');
        }
    } catch (err) {
        showError(errorDiv, 'Erreur de connexion au serveur');
    }
}

// Fonction d'inscription
async function register(e) {
    e.preventDefault();
    
    const nom = document.getElementById('reg-nom').value;
    const prenom = document.getElementById('reg-prenom').value;
    const email = document.getElementById('reg-email').value;
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    const confirmPassword = document.getElementById('reg-confirm-password').value;
    const errorDiv = document.getElementById('register-error');

    // Validation - utilisation de validateRegistration au lieu de validateRegisterForm
    if (!validateRegistration(nom, prenom, email, username, password, confirmPassword, errorDiv)) {
        return;
    }
    
    try {
        const response = await fetch('/api/users', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                nom, 
                prenom, 
                email, 
                username, 
                password 
            })
        });
        
        const data = await response.json();
        console.log('Réponse:', data);
        
        if (response.status === 201) {  // 201 = Created
            alert('✅ Inscription réussie !');
            window.location.href = '/login?registered=true';
        } else {
            errorDiv.style.display = 'block';
            errorDiv.textContent = data.error || 'Inscription échouée';
        }
    } catch (err) {
        console.error('Erreur:', err);
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Erreur de connexion au serveur';
    }
}

// Validation de l'inscription
function validateRegistration(nom, prenom, email, username, password, confirmPassword, errorDiv) {
    if (!nom || !prenom || !email || !username || !password) {
        showError(errorDiv, 'Tous les champs sont requis');
        return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showError(errorDiv, 'Email invalide');
        return false;
    }

    if (password.length < 6) {
        showError(errorDiv, 'Le mot de passe doit contenir au moins 6 caractères');
        return false;
    }

    if (password !== confirmPassword) {
        showError(errorDiv, 'Les mots de passe ne correspondent pas');
        return false;
    }

    hideError(errorDiv);
    return true;
}

function showError(element, message) {
    element.style.display = 'block';
    element.textContent = message;
}

function hideError(element) {
    element.style.display = 'none';
}