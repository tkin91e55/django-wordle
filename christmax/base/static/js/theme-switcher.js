/**
 * Theme Switcher for Bootstrap 5.3+ Dark Mode
 * 
 * Handles light/dark mode toggle with localStorage persistence.
 * No custom CSS required - uses Bootstrap's built-in dark mode.
 */

/**
 * Toggle between light and dark themes.
 */
function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-bs-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';

  html.setAttribute('data-bs-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeIcon(newTheme);
}

/**
 * Update the theme icon based on current theme.
 *
 * @param {string} theme - The current theme ('light' or 'dark')
 */
function updateThemeIcon(theme) {
  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.className = theme === 'light' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
  }
}

/**
 * Initialize theme on page load.
 * Loads saved theme from localStorage or defaults to 'light'.
 */
function initTheme() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-bs-theme', savedTheme);
  updateThemeIcon(savedTheme);
}

// Initialize theme when DOM is ready
document.addEventListener('DOMContentLoaded', initTheme);
