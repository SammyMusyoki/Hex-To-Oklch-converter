from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from color_converter import ColorConverter
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

converter = ColorConverter()

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML file"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files from frontend"""
    return send_from_directory('../frontend', filename)

@app.route('/api/convert-colors', methods=['POST'])
def convert_colors():
    """Convert hex colors to OKLCH and generate theme"""
    try:
        data = request.get_json()
        
        primary_hex = data.get('primary')
        dark_hex = data.get('dark') 
        light_hex = data.get('light')
        
        if not all([primary_hex, dark_hex, light_hex]):
            return jsonify({'error': 'All three colors are required'}), 400
        
        # Convert colors to OKLCH
        primary_oklch = converter.hex_to_oklch(primary_hex)
        dark_oklch = converter.hex_to_oklch(dark_hex)
        light_oklch = converter.hex_to_oklch(light_hex)
        
        # Generate complete theme variables matching globals.css structure
        theme_vars = {
            'light': {
                'radius': '0.65rem',
                'background': 'oklch(1 0 0)',  # Pure white
                'foreground': 'oklch(0.141 0.005 285.823)',  # Dark text
                'card': 'oklch(1 0 0)',  # Pure white
                'card-foreground': 'oklch(0.141 0.005 285.823)',  # Dark text
                'popover': 'oklch(1 0 0)',  # Pure white
                'popover-foreground': 'oklch(0.141 0.005 285.823)',  # Dark text
                'primary': converter.format_oklch_css(primary_oklch),
                'primary-foreground': 'oklch(0.969 0.016 293.756)',  # Light text on primary
                'secondary': 'oklch(0.967 0.001 286.375)',  # Light gray
                'secondary-foreground': 'oklch(0.21 0.006 285.885)',  # Dark gray text
                'muted': 'oklch(0.967 0.001 286.375)',  # Light gray
                'muted-foreground': 'oklch(0.552 0.016 285.938)',  # Medium gray text
                'accent': 'oklch(0.967 0.001 286.375)',  # Light gray
                'accent-foreground': 'oklch(0.21 0.006 285.885)',  # Dark gray text
                'destructive': 'oklch(0.577 0.245 27.325)',  # Red
                'border': 'oklch(0.92 0.004 286.32)',  # Light border
                'input': 'oklch(0.92 0.004 286.32)',  # Light input border
                'ring': converter.format_oklch_css(primary_oklch),
                'chart-1': 'oklch(0.646 0.222 41.116)',
                'chart-2': 'oklch(0.6 0.118 184.704)',
                'chart-3': 'oklch(0.398 0.07 227.392)',
                'chart-4': 'oklch(0.828 0.189 84.429)',
                'chart-5': 'oklch(0.769 0.188 70.08)',
                'sidebar': 'oklch(0.985 0 0)',  # Pure white
                'sidebar-foreground': 'oklch(0.141 0.005 285.823)',  # Dark text
                'sidebar-primary': converter.format_oklch_css(primary_oklch),
                'sidebar-primary-foreground': 'oklch(0.969 0.016 293.756)',
                'sidebar-accent': 'oklch(0.967 0.001 286.375)',  # Light gray
                'sidebar-accent-foreground': 'oklch(0.21 0.006 285.885)',  # Dark gray text
                'sidebar-border': 'oklch(0.92 0.004 286.32)',  # Light border
                'sidebar-ring': converter.format_oklch_css(primary_oklch),
            },
            'dark': {
                'background': 'oklch(0.141 0.005 285.823)',  # Dark background
                'foreground': 'oklch(0.985 0 0)',  # White text
                'card': 'oklch(0.21 0.006 285.885)',  # Dark card
                'card-foreground': 'oklch(0.985 0 0)',  # White text
                'popover': 'oklch(0.21 0.006 285.885)',  # Dark popover
                'popover-foreground': 'oklch(0.985 0 0)',  # White text
                'primary': converter.format_oklch_css(converter.adjust_primary_for_dark(primary_oklch)),
                'primary-foreground': 'oklch(0.969 0.016 293.756)',
                'secondary': 'oklch(0.274 0.006 286.033)',  # Dark gray
                'secondary-foreground': 'oklch(0.985 0 0)',  # White text
                'muted': 'oklch(0.274 0.006 286.033)',  # Dark gray
                'muted-foreground': 'oklch(0.705 0.015 286.067)',  # Light gray text
                'accent': 'oklch(0.274 0.006 286.033)',  # Dark gray
                'accent-foreground': 'oklch(0.985 0 0)',  # White text
                'destructive': 'oklch(0.704 0.191 22.216)',  # Red
                'border': 'oklch(1 0 0 / 10%)',  # White with opacity
                'input': 'oklch(1 0 0 / 15%)',  # White with opacity
                'ring': converter.format_oklch_css(converter.adjust_primary_for_dark(primary_oklch)),
                'chart-1': 'oklch(0.488 0.243 264.376)',
                'chart-2': 'oklch(0.696 0.17 162.48)',
                'chart-3': 'oklch(0.769 0.188 70.08)',
                'chart-4': 'oklch(0.627 0.265 303.9)',
                'chart-5': 'oklch(0.645 0.246 16.439)',
                'sidebar': 'oklch(0.21 0.006 285.885)',  # Dark sidebar
                'sidebar-foreground': 'oklch(0.985 0 0)',  # White text
                'sidebar-primary': converter.format_oklch_css(converter.adjust_primary_for_dark(primary_oklch)),
                'sidebar-primary-foreground': 'oklch(0.969 0.016 293.756)',
                'sidebar-accent': 'oklch(0.274 0.006 286.033)',  # Dark gray
                'sidebar-accent-foreground': 'oklch(0.985 0 0)',  # White text
                'sidebar-border': 'oklch(1 0 0 / 10%)',  # White with opacity
                'sidebar-ring': converter.format_oklch_css(converter.adjust_primary_for_dark(primary_oklch)),
            }
        }
        
        return jsonify({
            'success': True,
            'theme': theme_vars,
            'conversions': {
                'primary': converter.format_oklch_css(primary_oklch),
                'dark': converter.format_oklch_css(dark_oklch),
                'light': converter.format_oklch_css(light_oklch)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test')
def test_api():
    """Test endpoint"""
    return jsonify({'message': 'API is working!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

