// login.js - Funcionalidades adicionales para el sistema de login

document.addEventListener('DOMContentLoaded', function() {
    // Auto-ocultar mensajes después de 5 segundos
    const messages = document.querySelectorAll('[role="alert"]');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s ease-out';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
    
    // Validación en tiempo real del formulario de login
    const form = document.querySelector('form');
    const usernameField = document.querySelector('input[name="username"]');
    const passwordField = document.querySelector('input[name="password"]');
    const submitButton = document.querySelector('button[type="submit"]');
    
    if (form && usernameField && passwordField && submitButton) {
        // Función para validar el formulario
        function validateForm() {
            const username = usernameField.value.trim();
            const password = passwordField.value.trim();
            
            if (username.length >= 3 && password.length >= 6) {
                submitButton.disabled = false;
                submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
                submitButton.classList.add('hover:bg-indigo-700');
            } else {
                submitButton.disabled = true;
                submitButton.classList.add('opacity-50', 'cursor-not-allowed');
                submitButton.classList.remove('hover:bg-indigo-700');
            }
        }
        
        // Agregar event listeners
        usernameField.addEventListener('input', validateForm);
        passwordField.addEventListener('input', validateForm);
        
        // Validación inicial
        validateForm();
        
        // Mostrar/ocultar contraseña
        const passwordContainer = passwordField.parentElement;
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.innerHTML = '👁️';
        toggleButton.className = 'absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600';
        toggleButton.style.cssText = 'background: none; border: none; cursor: pointer;';
        
        passwordContainer.style.position = 'relative';
        passwordContainer.appendChild(toggleButton);
        
        toggleButton.addEventListener('click', function() {
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                toggleButton.innerHTML = '🙈';
            } else {
                passwordField.type = 'password';
                toggleButton.innerHTML = '👁️';
            }
        });
    }
    
    // Efecto de carga en el botón de envío
    if (form) {
        form.addEventListener('submit', function() {
            submitButton.innerHTML = 'Iniciando sesión...';
            submitButton.disabled = true;
            submitButton.classList.add('opacity-50', 'cursor-not-allowed');
        });
    }
});
