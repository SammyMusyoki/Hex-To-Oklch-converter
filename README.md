# OKLCH Theme Generator

Convert hex colors to accurate OKLCH values and generate complete CSS themes.

## Project Structure
```
├── api/                 # Python Flask backend
│   ├── app.py          # Main Flask application
│   ├── color_converter.py  # Color conversion logic
│   └── requirements.txt     # Python dependencies
├── frontend/           # HTML/CSS/JS frontend
│   ├── index.html      # Main UI
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
└── README.md
```

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
1. Enter three hex colors (primary, light base, dark base)
2. Click "Generate OKLCH Theme"
3. Copy the generated CSS variables

Dark Purple (#7C3AED), Light Purple(#A855F7) and Primary Purple (#8B42E6)

"# Hex-To-Oklch-converter" 
