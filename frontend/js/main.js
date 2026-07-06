//Main JavaScript

//DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Mental Health Support System loaded successfully!');
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize form validation
    initFormValidation();
    
    // Initialize auto-dismiss alerts
    initAlerts();
    
    // Initialize mood buttons
    initMoodButtons();
});

//Tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length > 0) {
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
}

//Form Validation
function initFormValidation() {
    // Password confirmation validation
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    if (password && confirmPassword) {
        confirmPassword.addEventListener('input', function() {
            if (password.value !== this.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Email validation
    const email = document.getElementById('email');
    if (email) {
        email.addEventListener('input', function() {
            if (this.validity.typeMismatch) {
                this.setCustomValidity('Please enter a valid email address');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}

//Alerts
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            });
        }, 5000);
    }
}

//Mood Buttons
function initMoodButtons() {
    const moodBtns = document.querySelectorAll('.mood-btn');
    const moodInput = document.getElementById('selectedMood');
    
    if (moodBtns.length > 0 && moodInput) {
        moodBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active class from all
                moodBtns.forEach(b => b.classList.remove('active'));
                // Add active class to clicked
                this.classList.add('active');
                // Set value
                moodInput.value = this.dataset.mood;
            });
        });
    }
}

//Time Slot Selection
function initTimeSlots() {
    const slots = document.querySelectorAll('.time-slot:not([disabled])');
    const timeInput = document.getElementById('selectedTime');
    
    if (slots.length > 0 && timeInput) {
        slots.forEach(slot => {
            slot.addEventListener('click', function() {
                slots.forEach(s => s.classList.remove('active'));
                this.classList.add('active');
                timeInput.value = this.dataset.time;
            });
        });
    }
}

//Assessment Progress
function updateAssessmentProgress() {
    const radios = document.querySelectorAll('input[type="radio"]');
    const progressBar = document.getElementById('progressBar');
    
    if (radios.length > 0 && progressBar) {
        radios.forEach(radio => {
            radio.addEventListener('change', function() {
                const totalQuestions = document.querySelectorAll('.question-item').length;
                let answered = 0;
                
                for (let i = 1; i <= totalQuestions; i++) {
                    const checked = document.querySelector(`input[name="q${i}"]:checked`);
                    if (checked) answered++;
                }
                
                const percent = Math.round((answered / totalQuestions) * 100);
                progressBar.style.width = percent + '%';
                progressBar.textContent = percent + '%';
                
                // Change color based on progress
                if (percent === 100) {
                    progressBar.classList.remove('bg-warning', 'bg-danger');
                    progressBar.classList.add('bg-success');
                } else if (percent >= 50) {
                    progressBar.classList.remove('bg-danger');
                    progressBar.classList.add('bg-warning');
                } else {
                    progressBar.classList.remove('bg-success', 'bg-warning');
                    progressBar.classList.add('bg-danger');
                }
            });
        });
    }
}

//Password Toggle Visibility
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);
    }
}

//Confirmation Dialog
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Toast Notificatio
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        // Create container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.role = 'alert';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.getElementById('toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Mental Health Support System loaded successfully!');
});

//Export Functions
// Make functions available globally
window.togglePasswordVisibility = togglePasswordVisibility;
window.confirmAction = confirmAction;
window.showToast = showToast;