// Toggle logic listening for button actions to switch document node attributes
document.getElementById('theme-toggle').addEventListener('click', () => {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme');
    root.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');
});