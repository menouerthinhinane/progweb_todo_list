// Fonction utilitaire pour les appels API
async function apiCall(url, method, body) {
    const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: body ? JSON.stringify(body) : undefined
    });
    return res.json();
}

// Validation des champs d'inscription
function validateRegisterForm() {
    const nom = document.getElementById('reg-nom').value;
    const prenom = document.getElementById('reg-prenom').value;
    const email = document.getElementById('reg-email').value;
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    const confirmPassword = document.getElementById('reg-confirm-password').value;
    const errorDiv = document.getElementById('register-error');

    // Vérification des champs vides
    if (!nom || !prenom || !email || !username || !password) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Tous les champs sont requis';
        return false;
    }

    // Validation email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Email invalide';
        return false;
    }

    // Validation mot de passe (minimum 6 caractères)
    if (password.length < 6) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Le mot de passe doit contenir au moins 6 caractères';
        return false;
    }

    // Vérification confirmation mot de passe
    if (password !== confirmPassword) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = 'Les mots de passe ne correspondent pas';
        return false;
    }

    errorDiv.style.display = 'none';
    return true;
}

// Fonction d'inscription
async function register() {
    const nom = document.getElementById('reg-nom').value;
    const prenom = document.getElementById('reg-prenom').value;
    const email = document.getElementById('reg-email').value;
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    
    try {
        const res = await fetch('/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await res.json();
        console.log('Réponse:', data);
        
        if (res.status === 201) {
            alert('✅ Inscription réussie !');
            window.location.href = '/login';
        } else {
            alert('❌ Erreur: ' + (data.error || 'Inscription échouée'));
        }
    } catch (err) {
        console.error('Erreur:', err);
        alert('❌ Erreur de connexion au serveur');
    }
}

// Fonction de connexion
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        document.getElementById('login-error').style.display = 'block';
        document.getElementById('login-error').textContent = 'Veuillez remplir tous les champs';
        return;
    }

    try {
        const data = await apiCall('/api/users/login', 'POST', { username, password });
        
        if (data.id) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('username', data.username);
            localStorage.setItem('userId', data.id);
            window.location.href = '/tasks';
        } else {
            document.getElementById('login-error').style.display = 'block';
            document.getElementById('login-error').textContent = data.error || 'Identifiants incorrects';
        }
    } catch (err) {
        console.error('Erreur:', err);
        document.getElementById('login-error').style.display = 'block';
        document.getElementById('login-error').textContent = 'Erreur de connexion au serveur';
    }
}

// Vérifier si l'utilisateur est connecté au chargement
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname;

    // Rediriger vers login si non connecté (sauf sur les pages publiques)
    if (!token && !['/login', '/register'].includes(currentPage)) {
        window.location.href = '/login';
    }
});