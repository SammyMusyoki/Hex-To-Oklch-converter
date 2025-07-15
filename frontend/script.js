const API_BASE = 'http://localhost:5000/api';

// Sync color picker with hex input
document.addEventListener('DOMContentLoaded', function() {
    const colorInputs = [
        { picker: 'primary', hex: 'primaryHex' },
        { picker: 'light', hex: 'lightHex' },
        { picker: 'dark', hex: 'darkHex' }
    ];
    
    colorInputs.forEach(({ picker, hex }) => {
        const pickerEl = document.getElementById(picker);
        const hexEl = document.getElementById(hex);
        
        pickerEl.addEventListener('change', () => {
            hexEl.value = pickerEl.value;
        });
        
        hexEl.addEventListener('input', () => {
            if (isValidHex(hexEl.value)) {
                pickerEl.value = hexEl.value;
            }
        });
    });
});

function isValidHex(hex) {
    return /^#[0-9A-F]{6}$/i.test(hex);
}

document.getElementById('colorForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const primary = document.getElementById('primaryHex').value;
    const light = document.getElementById('lightHex').value;
    const dark = document.getElementById('darkHex').value;
    
    // Validate hex codes
    if (!isValidHex(primary) || !isValidHex(light) || !isValidHex(dark)) {
        showError('Please enter valid hex color codes');
        return;
    }
    
    showLoading(true);
    hideError();
    hideOutput();
    
    try {
        const response = await fetch(`${API_BASE}/convert-colors`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                primary: primary,
                light: light,
                dark: dark
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.theme);
        } else {
            showError(data.error || 'Conversion failed');
        }
        
    } catch (error) {
        showError('Failed to connect to API: ' + error.message);
    } finally {
        showLoading(false);
    }
});

function displayResults(theme) {
    const lightThemeCSS = generateCSSVariables(theme.light, 'Light Theme');
    const darkThemeCSS = generateCSSVariables(theme.dark, 'Dark Theme');
    
    document.getElementById('lightTheme').textContent = lightThemeCSS;
    document.getElementById('darkTheme').textContent = darkThemeCSS;
    
    showOutput();
}

function generateCSSVariables(colors, themeName) {
    const selector = themeName.includes('Dark') ? '.dark' : ':root';
    let css = `${selector} {\n`;
    
    for (const [name, value] of Object.entries(colors)) {
        css += `  --${name}: ${value};\n`;
    }
    
    css += '}';
    return css;
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    const button = event.target; // Get button reference here
    
    // Try modern clipboard API first
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showCopySuccess(button);
        }).catch(err => {
            console.error('Clipboard API failed: ', err);
            fallbackCopyTextToClipboard(text, button);
        });
    } else {
        // Fallback for older browsers or non-HTTPS
        fallbackCopyTextToClipboard(text, button);
    }
}

function fallbackCopyTextToClipboard(text, button) {
    // Create temporary textarea
    const textArea = document.createElement("textarea");
    textArea.value = text;
    
    // Make it invisible but accessible
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess(button);
        } else {
            showToast('Failed to copy to clipboard', 'error');
        }
    } catch (err) {
        console.error('Fallback copy failed: ', err);
        showToast('Copy not supported in this browser', 'error');
    }
    
    document.body.removeChild(textArea);
}

function showCopySuccess(button) {
    // Show success feedback on button
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.classList.add('copied');
    
    // Show toast notification
    showToast('Theme copied to clipboard!');
    
    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('copied');
    }, 2000);
}

function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showError(message) {
    const errorEl = document.getElementById('error');
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function showOutput() {
    document.getElementById('output').classList.remove('hidden');
}

function hideOutput() {
    document.getElementById('output').classList.add('hidden');
}

function showToast(message, type = 'success') {
    // Remove existing toast if any
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Add to body
    document.body.appendChild(toast);
    
    // Show toast with animation
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Hide and remove toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


