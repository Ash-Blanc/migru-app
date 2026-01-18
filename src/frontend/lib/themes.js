// Light Theme (Nord-inspired with adjustments for migraine sensitivity)
// Focusing on low contrast glare, soft colors
const lightTheme = {
  "color-scheme": "light",
  "primary": "#5E81AC",          // Muted Blue
  "primary-content": "#ECEFF4",  // Snow White
  "secondary": "#81A1C1",        // Lighter Blue
  "secondary-content": "#2E3440",// Dark Grey
  "accent": "#88C0D0",           // Cyan
  "accent-content": "#2E3440",
  "neutral": "#3B4252",          // Dark Grey
  "neutral-content": "#ECEFF4",
  "base-100": "#ECEFF4",         // Snow White
  "base-200": "#E5E9F0",         // Slightly darker
  "base-300": "#D8DEE9",         // Even darker
  "base-content": "#2E3440",     // Dark Grey text (not black)
  "info": "#5E81AC",
  "success": "#A3BE8C",          // Muted Green
  "warning": "#EBCB8B",          // Muted Yellow
  "error": "#BF616A",            // Muted Red
  
  "--rounded-box": "1rem",
  "--rounded-btn": "0.5rem",
  "--rounded-badge": "1.9rem",
  "--animation-btn": "0.25s",
  "--animation-input": "0.2s",
  "--btn-focus-scale": "0.95",
  "--border-btn": "1px",
  "--tab-border": "1px",
  "--tab-radius": "0.5rem",
  
  // Custom Vars for Migraine specific UI
  "--risk-low": "154 54% 64%",      // Muted Green (HSL)
  "--risk-moderate": "40 71% 73%",  // Muted Yellow (HSL)
  "--risk-high": "355 45% 56%",     // Muted Red (HSL)
};

// Dark Theme (Deep Blue/Grey - very low light emission)
const darkTheme = {
  "color-scheme": "dark",
  "primary": "#88C0D0",          // Cyan
  "primary-content": "#2E3440",
  "secondary": "#81A1C1",
  "secondary-content": "#2E3440",
  "accent": "#B48EAD",           // Purple
  "accent-content": "#ECEFF4",
  "neutral": "#2E3440",          // Deep Grey
  "neutral-content": "#ECEFF4",
  "base-100": "#1C212B",         // Almost Black Blue (Custom)
  "base-200": "#161A22",         // Darker
  "base-300": "#101319",         // Darkest
  "base-content": "#D8DEE9",     // Off-white text
  "info": "#88C0D0",
  "success": "#A3BE8C",
  "warning": "#EBCB8B",
  "error": "#BF616A",
  
  "--rounded-box": "1rem",
  "--rounded-btn": "0.5rem",
  "--rounded-badge": "1.9rem",
  "--animation-btn": "0.25s",
  "--animation-input": "0.2s",
  "--btn-focus-scale": "0.95",
  "--border-btn": "1px",
  "--tab-border": "1px",
  "--tab-radius": "0.5rem",

  // Custom Vars for Migraine specific UI
  "--risk-low": "154 44% 54%",
  "--risk-moderate": "40 61% 63%",
  "--risk-high": "355 35% 46%",
};

export { lightTheme, darkTheme };
