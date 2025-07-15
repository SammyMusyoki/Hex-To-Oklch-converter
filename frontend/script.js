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
    
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const button = event.target;
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    });
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