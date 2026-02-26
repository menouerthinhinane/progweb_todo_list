// Version simplifiée de auth.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ auth.js chargé !');
    
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        console.log('✅ Formulaire trouvé');
        
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('📤 Soumission du formulaire');
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('login-error');
            
            try {
                console.log('📡 Envoi requête à /api/users/login');
                
                const response = await fetch('/api/users/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                console.log('📥 Réponse reçue:', data);
                
                if (response.ok && data.token) {
                    console.log('✅ Connexion réussie !');
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('username', data.username);
                    localStorage.setItem('userId', data.id);
                    window.location.href = '/tasks';
                } else {
                    console.log('❌ Erreur:', data.error);
                    errorDiv.style.display = 'block';
                    errorDiv.textContent = data.error || 'Identifiants incorrects';
                }
            } catch (err) {
                console.error('🔥 Erreur réseau:', err);
                errorDiv.style.display = 'block';
                errorDiv.textContent = 'Erreur de connexion au serveur';
            }
        });
    } else {
        console.error('❌ Formulaire non trouvé !');
    }
});
