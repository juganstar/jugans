document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;
    
    // Check for saved preference or system preference
    const savedMode = localStorage.getItem('darkMode');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial mode
    if (savedMode === 'enabled' || (!savedMode && systemPrefersDark)) {
        htmlElement.classList.add('dark-mode');
        darkModeToggle.textContent = '🌞';
    }
    
    // Toggle functionality
    darkModeToggle.addEventListener('click', function() {
        htmlElement.classList.toggle('dark-mode');
        const isDark = htmlElement.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
        darkModeToggle.textContent = isDark ? '🌞' : '🌙';
    });
    
    // Listen for system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('darkMode')) {
            htmlElement.classList.toggle('dark-mode', e.matches);
            darkModeToggle.textContent = e.matches ? '🌞' : '🌙';
        }
    });
});
