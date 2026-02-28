let currentFilter = 'all';
// Fonction pour vérifier l'authentification
function isAuthenticated() {
    return !!localStorage.getItem('token');
}

// Fonction utilitaire pour les appels API
async function apiCall(url, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const responseData = await response.json();
        return {
            ok: response.ok,
            data: responseData,
            status: response.status
        };
    } catch (error) {
        console.error('API Error:', error);
        return {
            ok: false,
            data: { error: error.message },
            status: 500
        };
    }
}

// Fonctions utilitaires pour l'échappement HTML et le formatage des dates
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Vérifier l'authentification
    if (!isAuthenticated()) {
        window.location.href = '/login';
        return;
    }
    
    // Initialiser la date minimum
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('task-date');
    if (dateInput) {
        dateInput.setAttribute('min', today);
    }
    
    // Afficher la date du jour
    const dateDisplay = document.getElementById('current-date');
    if (dateDisplay) {
        dateDisplay.textContent = new Date().toLocaleDateString('fr-FR', {
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric'
        });
    }
    
    // Afficher le nom d'utilisateur
    const userNameSpan = document.getElementById('user-name');
    if (userNameSpan) {
        userNameSpan.textContent = localStorage.getItem('username') || 'Utilisateur';
    }
    
    // Écouteurs d'événements
    const taskForm = document.getElementById('task-form');
    if (taskForm) {
        taskForm.addEventListener('submit', addTask);
    }
    
    // Filtres
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            setFilter(this.dataset.filter);
        });
    });
    
    // Charger les tâches
    loadTasks();
});

// Charger les tâches
async function loadTasks() {
    const taskList = document.getElementById('task-list');
    const emptyState = document.getElementById('empty-state');
    const spinner = document.getElementById('loading-spinner');
    
    if (!taskList) return;
    
    showSpinner(true);
    taskList.innerHTML = '';
    
    try {
        const { ok, data } = await apiCall('/api/tasks', 'GET');
        
        showSpinner(false);
        
        if (!ok || !data || data.length === 0) {
            showEmptyState(true);
            return;
        }
        
        showEmptyState(false);
        displayTasks(data);
    } catch (error) {
        console.error('Erreur:', error);
        showSpinner(false);
        showEmptyState(true, '❌ Erreur de chargement');
    }
}

// Afficher les tâches selon le filtre
function displayTasks(tasks) {
    const taskList = document.getElementById('task-list');
    if (!taskList) return;
    
    taskList.innerHTML = '';
    
    const filteredTasks = filterTasksByStatus(tasks, currentFilter);
    
    if (filteredTasks.length === 0) {
        showEmptyState(true);
        return;
    }
    
    showEmptyState(false);
    
    // Trier les tâches
    filteredTasks.sort(sortTasks);
    
    filteredTasks.forEach(task => {
        taskList.appendChild(createTaskElement(task));
    });
}

// Filtrer les tâches par statut
function filterTasksByStatus(tasks, filter) {
    return tasks.filter(task => {
        if (filter === 'active') return !task.completed;
        if (filter === 'completed') return task.completed;
        return true;
    });
}

// Trier les tâches
function sortTasks(a, b) {
    // Tâches non terminées d'abord
    if (a.completed !== b.completed) {
        return a.completed ? 1 : -1;
    }
    // Puis par date (plus récent d'abord)
    return new Date(b.created_at) - new Date(a.created_at);
}

// Créer un élément de tâche
function createTaskElement(task) {
    const li = document.createElement('li');
    li.className = `task-item ${task.completed ? 'completed' : ''}`;
    li.setAttribute('data-id', task.id);
    
    // Vérifier si la tâche est en retard
    const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.completed;
    
    li.innerHTML = `
        <div class="task-checkbox">
            <input type="checkbox" 
                   ${task.completed ? 'checked' : ''} 
                   onchange="toggleTask(${task.id})"
                   class="task-checkbox-input">
        </div>
        <div class="task-content">
            <div class="task-title ${task.completed ? 'completed-text' : ''}">
                ${escapeHtml(task.title)}
            </div>
            ${task.description ? `
                <div class="task-description">${escapeHtml(task.description)}</div>
            ` : ''}
            <div class="task-meta">
                <span class="task-date ${isOverdue ? 'overdue' : ''}">
                      ${task.due_date ? formatDate(task.due_date) : 'Pas de date'}
                    ${isOverdue ? ' (En retard)' : ''}
                </span>
                <span class="task-created">
                    Créée le ${formatDate(task.created_at)}
                </span>
            </div>
        </div>
        <div class="task-actions">
            <button onclick="deleteTask(${task.id})" class="btn-delete" title="Supprimer">🗑️</button>
        </div>
    `;
    
    return li;
}

// Ajouter une tâche
async function addTask(e) {
    e.preventDefault();
    
    const title = document.getElementById('task-title').value.trim();
    const description = document.getElementById('task-description').value.trim();
    const dueDate = document.getElementById('task-date').value;
    
    if (!title) {
        alert('Le titre est obligatoire');
        return;
    }
    
    // Vérifier que la date n'est pas antérieure à aujourd'hui
    if (dueDate) {
        const today = new Date().toISOString().split('T')[0];
        if (dueDate < today) {
            alert('La date ne peut pas être antérieure à aujourd\'hui');
            return;
        }
    }
    
    try {
        const { ok } = await apiCall('/api/tasks', 'POST', {
            title,
            description: description || null,
            due_date: dueDate || null
        });
        
        if (ok) {
            // Réinitialiser le formulaire
            document.getElementById('task-title').value = '';
            document.getElementById('task-description').value = '';
            document.getElementById('task-date').value = '';
            
            loadTasks();
        } else {
            alert('Erreur lors de l\'ajout de la tâche');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur de connexion au serveur');
    }
}

async function toggleTask(taskId) {
    try {
        const { ok } = await apiCall(`/api/tasks/${taskId}`, 'PUT', { completed: true });
        
        if (ok) {
            loadTasks(); 
        } else {
            alert('Erreur lors de la mise à jour');
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// Supprimer une tâche
async function deleteTask(taskId) {
    if (!confirm('Voulez-vous vraiment supprimer cette tâche ?')) {
        return;
    }
    
    try {
        const { ok } = await apiCall(`/api/tasks/${taskId}`, 'DELETE');
        
        if (ok) {
            loadTasks(); 
        } else {
            alert('Erreur lors de la suppression');
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// Changer le filtre
function setFilter(filter) {
    currentFilter = filter;
    
    // Mettre à jour les boutons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.dataset.filter === filter) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    loadTasks();
}

// Afficher/masquer le spinner
function showSpinner(show) {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = show ? 'block' : 'none';
    }
}

// Afficher/masquer l'état vide
function showEmptyState(show, message = '✨ Aucune tâche à afficher') {
    const emptyState = document.getElementById('empty-state');
    const taskList = document.getElementById('task-list');
    
    if (emptyState) {
        emptyState.style.display = show ? 'block' : 'none';
        if (show && message) {
            emptyState.innerHTML = `<p>${message}</p><small>Créez votre première tâche ci-dessus !</small>`;
        }
    }
    
    if (taskList) {
        taskList.style.display = show ? 'none' : 'block';
    }
}
