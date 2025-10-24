/* * Este arquivo sobrescreve o script padrão do Django (theme.js) 
 * para forçar o uso do tema 'light' (claro), ignorando a preferência 
 * do sistema operacional do usuário.
 */
document.addEventListener('DOMContentLoaded', function() {
    // 1. Força a classe do body para tema claro (light)
    document.body.classList.remove('dark-mode');
    document.body.classList.add('light-mode');

    // 2. Tenta encontrar o botão de toggle de tema e o esconde
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.style.display = 'none';
    }

    // 3. Sobrescreve a função de inicialização do tema se ela existir
    if (window.addEventListener && document.documentElement.className.indexOf('dark-mode') > -1) {
        document.documentElement.className = document.documentElement.className.replace('dark-mode', 'light-mode');
    }
});