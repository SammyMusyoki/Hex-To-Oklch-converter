# OKLCH Tailwind@v4 Theme Generator

Convert hex colors to accurate OKLCH values and generate complete CSS themes with proper Oklab color space conversion.

## Project Structure
```
├── api/                 # Python Flask backend
│   ├── app.py          # Main Flask application
│   ├── color_converter.py  # Color conversion logic (Oklab-based)
│   └── requirements.txt     # Python dependencies
├── frontend/           # HTML/CSS/JS frontend
│   ├── index.html      # Main UI
│   ├── style.css       # Styling with toast notifications
│   └── script.js       # Frontend logic with clipboard functionality
└── README.md
```

## Features

- **Accurate OKLCH Conversion**: Uses proper Oklab color space for precise color conversion
- **Complete Theme Generation**: Generates light and dark theme CSS variables
- **Tailwind-Compatible**: Follows Tailwind CSS v4 color distribution patterns
- **Copy to Clipboard**: One-click copying with toast notifications and fallback support
- **Browser Compatibility**: Works across all modern browsers with fallback methods

## Setup & Run

1. Install Python dependencies:
```bash
cd api
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
python app.py
```

3. Open browser to: `http://localhost:5000`

## Usage

1. Enter three hex colors:
   - **Primary Color**: Main brand color (e.g., #8B42E6)
   - **Light Base**: Light theme base color (e.g., #A855F7) 
   - **Dark Base**: Dark theme base color (e.g., #7C3AED)

2. Click "Generate OKLCH Theme"

3. Copy the generated CSS variables using the copy buttons

## Example Colors

- **Primary Purple**: `#8B42E6` → `oklch(0.5601 0.2323 298.94)`
- **Light Purple**: `#A855F7` → `oklch(0.6268 0.2325 303.9)`
- **Dark Purple**: `#7C3AED` → `oklch(0.5413 0.2466 293.01)`

## Generated CSS Variables

The tool generates complete CSS custom properties for:
- Background and foreground colors
- Primary, secondary, muted, and accent colors
- Border, input, and ring colors
- Destructive (error) colors
- Chart colors for data visualization
- Sidebar-specific color variants
- Both light and dark theme variants

## Technical Details

- Uses `colour-science` library for accurate color space conversions
- Implements proper Oklab → OKLCH conversion pipeline
- Follows Tailwind CSS color distribution patterns
- Generates neutral grays with ~286° hue for non-primary elements

