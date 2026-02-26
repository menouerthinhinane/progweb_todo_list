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

// Fonction de connexion (déjà existante)
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
        console.log('📡 Envoi requête login...');
        
        const response = await fetch('/api/users/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        console.log('📥 Réponse:', data);
        
        if (response.ok && data.token) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('username', data.username);
            localStorage.setItem('userId', data.id);
            window.location.href = '/tasks';
        } else {
            showError(errorDiv, data.error || 'Identifiants incorrects');
        }
    } catch (err) {
        console.error('🔥 Erreur:', err);
        showError(errorDiv, 'Erreur de connexion au serveur');
    }
}

// === NOUVELLE FONCTION REGISTER (remplace l'ancienne) ===
async function register(e) {
    e.preventDefault();
    
    const nom = document.getElementById('reg-nom').value;
    const prenom = document.getElementById('reg-prenom').value;
    const email = document.getElementById('reg-email').value;
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    const confirmPassword = document.getElementById('reg-confirm-password').value;
    const errorDiv = document.getElementById('register-error');

    // Validation
    if (!nom || !prenom || !email || !username || !password) {
        showError(errorDiv, 'Tous les champs sont requis');
        return;
    }

    if (password !== confirmPassword) {
        showError(errorDiv, 'Les mots de passe ne correspondent pas');
        return;
    }

    try {
        // ⚠️ IMPORTANT: N'envoyer que username, email, password
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                username: username,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.status === 201) {
            alert('✅ Inscription réussie !');
            window.location.href = '/login?registered=true';
        } else {
            showError(errorDiv, data.error || 'Inscription échouée');
        }
    } catch (err) {
        console.error('Erreur:', err);
        showError(errorDiv, 'Erreur de connexion au serveur');
    }
}
// === FIN DE LA NOUVELLE FONCTION ===

// Fonctions utilitaires (déjà existantes)
function showError(element, message) {
    element.style.display = 'block';
    element.textContent = message;
}

function hideError(element) {
    element.style.display = 'none';
}
