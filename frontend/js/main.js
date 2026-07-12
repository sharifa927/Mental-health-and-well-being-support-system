// Main JavaScript (layout + existing helpers)

function bindLayoutEvents() {
    const sidebar = document.getElementById('appSidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    const collapseBtn = document.getElementById('sidebarCollapseBtn');
    const mobileSidebarBtn = document.getElementById('mobileSidebarBtn');

    // Sidebar collapse (desktop)
    if (collapseBtn && sidebar) {
        collapseBtn.addEventListener('click', () => {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    // Mobile drawer open/close
    if (mobileSidebarBtn && sidebar) {
        mobileSidebarBtn.addEventListener('click', () => {
            document.body.classList.toggle('sidebar-open');
            if (backdrop) backdrop.classList.toggle('show');
        });
    }

    if (backdrop) {
        backdrop.addEventListener('click', () => {
            document.body.classList.remove('sidebar-open');
            backdrop.classList.remove('show');
        });
    }

    // Settings submenu toggle
    const settingsToggle = document.querySelector('[data-group-toggle="settings"]');
    const settingsSubmenu = document.getElementById('settingsSubmenu');
    if (settingsToggle && settingsSubmenu) {
        settingsToggle.addEventListener('click', (e) => {
            // prevent unintended focus
            e.preventDefault();
            const show = settingsSubmenu.classList.toggle('show');
            settingsToggle.setAttribute('aria-expanded', show ? 'true' : 'false');
        });
    }

    // Close mobile drawer on navigation click
    document.querySelectorAll('.sidebar a').forEach(a => {
        a.addEventListener('click', () => {
            if (document.body.classList.contains('sidebar-open')) {
                document.body.classList.remove('sidebar-open');
                if (backdrop) backdrop.classList.remove('show');
            }
        });
    });

    // Active highlighting (best-effort)
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-link').forEach(link => {
        const href = link.getAttribute('href') || '';
        if (href && href !== '#' && currentPath === href) {
            link.classList.add('active');
        }
        // allow startsWith for nested admin pages
        if (href && href !== '#' && currentPath.startsWith(href) && href.length > 1) {
            link.classList.add('active');
        }
    });
}

//DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Mental Health Support System loaded successfully!');

    bindLayoutEvents();

    // Initialize tooltips
    initTooltips();

    // Initialize form validation
    initFormValidation();

    // Initialize auto-dismiss alerts
    initAlerts();

    // Initialize mood buttons
    initMoodButtons();

    // Assessment progress (if present)
    updateAssessmentProgress();

    // time slots (if present)
    initTimeSlots();

    // Settings submenu default aria
    const settingsToggle = document.querySelector('[data-group-toggle="settings"]');
    if (settingsToggle) settingsToggle.setAttribute('aria-expanded', 'false');
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
                moodBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
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

                const percent = totalQuestions > 0 ? Math.round((answered / totalQuestions) * 100) : 0;
                progressBar.style.width = percent + '%';
                progressBar.textContent = percent + '%';

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

//Export Functions (global)
window.togglePasswordVisibility = togglePasswordVisibility;
window.confirmAction = confirmAction;

