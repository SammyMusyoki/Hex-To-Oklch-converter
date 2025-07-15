import colour
import numpy as np
import re

class ColorConverter:
    def __init__(self):
        """Initialize the color converter"""
        pass
    
    def hex_to_oklch(self, hex_code):
        """
        Convert hex color to OKLCH with high accuracy using Oklab
        Returns: (lightness, chroma, hue) tuple
        """
        # Clean hex code
        hex_code = hex_code.lstrip('#').upper()
        
        if len(hex_code) != 6:
            raise ValueError("Invalid hex code format")
        
        # Convert hex to RGB (0-1 range)
        try:
            r = int(hex_code[0:2], 16) / 255.0
            g = int(hex_code[2:4], 16) / 255.0  
            b = int(hex_code[4:6], 16) / 255.0
            rgb = np.array([r, g, b])
        except ValueError:
            raise ValueError("Invalid hex characters")
        
        # Convert RGB to OKLCH using proper Oklab conversion
        try:
            # Step 1: RGB -> XYZ (using sRGB colorspace)
            xyz = colour.sRGB_to_XYZ(rgb)
            
            # Step 2: XYZ -> Oklab (proper OKLCH base)
            oklab = colour.XYZ_to_Oklab(xyz)
            
            # Step 3: Oklab -> OKLCH
            # Convert a,b to chroma and hue
            L = oklab[0]  # Lightness (already 0-1)
            a = oklab[1]  # Green-red axis
            b = oklab[2]  # Blue-yellow axis
            
            # Calculate chroma and hue from a,b
            C = np.sqrt(a*a + b*b)  # Chroma
            H = np.degrees(np.arctan2(b, a))  # Hue in degrees
            
            # Normalize hue to 0-360 range
            if H < 0:
                H += 360
            
            # Handle NaN values for achromatic colors
            if np.isnan(H):
                H = 0.0
            if np.isnan(C):
                C = 0.0
                
            oklch = np.array([L, C, H])
            return oklch
            
        except Exception as e:
            raise ValueError(f"Color conversion failed: {str(e)}")
    
    def format_oklch_css(self, oklch_values):
        """Format OKLCH values for CSS variables"""
        l, c, h = oklch_values
        
        # Handle NaN hue (for grays)
        if np.isnan(h):
            h = 0
            
        return f"oklch({l:.3f} {c:.3f} {h:.3f})"
    
    def generate_color_variations(self, base_oklch, variation_type="light"):
        """Generate color variations for theme"""
        l, c, h = base_oklch
        
        variations = {}
        
        if variation_type == "light":
            # Light theme variations
            variations['background'] = np.array([0.98, 0.005, h])
            variations['foreground'] = np.array([0.15, 0.01, h])
            variations['muted'] = np.array([0.95, 0.01, h])
            variations['border'] = np.array([0.9, 0.01, h])
        else:
            # Dark theme variations  
            variations['background'] = np.array([0.15, 0.01, h])
            variations['foreground'] = np.array([0.98, 0.005, h])
            variations['muted'] = np.array([0.25, 0.01, h])
            variations['border'] = np.array([0.3, 0.02, h])
            
        return variations
    
    def test_conversion(self):
        """Test the converter with known values"""
        test_colors = {
            "#8B42E6": "Primary Purple",
            "#A855F7": "Light Purple", 
            "#7C3AED": "Dark Purple",
            "#FFFFFF": "white",
            "#000000": "black"
        }
        
        print("Testing color conversions:")
        for hex_code, name in test_colors.items():
            try:
                oklch = self.hex_to_oklch(hex_code)
                css_format = self.format_oklch_css(oklch)
                print(f"{name} ({hex_code}): {css_format}")
                print(f"  L:{oklch[0]:.4f} C:{oklch[1]:.4f} H:{oklch[2]:.2f}")
            except Exception as e:
                print(f"Error converting {name}: {e}")

    def generate_muted_color(self, base_oklch, theme_type):
        """Generate muted color variations with neutral hue"""
        if theme_type == 'light':
            return np.array([0.967, 0.001, 286.375])  # Very light gray
        else:
            return np.array([0.274, 0.006, 286.033])  # Dark gray
    
    def generate_muted_foreground(self, base_oklch, theme_type):
        """Generate muted foreground colors with neutral hue"""
        if theme_type == 'light':
            return np.array([0.552, 0.016, 285.938])  # Medium gray
        else:
            return np.array([0.705, 0.015, 286.067])  # Light gray
    
    def generate_border_color(self, base_oklch, theme_type):
        """Generate border colors with neutral hue"""
        if theme_type == 'light':
            return np.array([0.92, 0.004, 286.32])  # Light border
        else:
            return np.array([1, 0, 0])  # White with opacity handled in CSS
    
    def generate_destructive_color(self, theme_type):
        """Generate destructive/error colors"""
        if theme_type == 'light':
            return np.array([0.577, 0.245, 27.325])
        else:
            return np.array([0.704, 0.191, 22.216])
    
    def generate_chart_color(self, chart_num, theme_type):
        """Generate chart colors"""
        light_charts = {
            1: [0.646, 0.222, 41.116],
            2: [0.6, 0.118, 184.704],
            3: [0.398, 0.07, 227.392],
            4: [0.828, 0.189, 84.429],
            5: [0.769, 0.188, 70.08]
        }
        dark_charts = {
            1: [0.488, 0.243, 264.376],
            2: [0.696, 0.17, 162.48],
            3: [0.769, 0.188, 70.08],
            4: [0.627, 0.265, 303.9],
            5: [0.645, 0.246, 16.439]
        }
        
        charts = light_charts if theme_type == 'light' else dark_charts
        return np.array(charts.get(chart_num, [0.5, 0.1, 0]))
    
    def generate_sidebar_bg(self, theme_type):
        """Generate sidebar background"""
        if theme_type == 'light':
            return np.array([0.985, 0, 0])  # Pure white
        else:
            return np.array([0.21, 0.006, 285.885])  # Dark sidebar
    
    def generate_card_bg(self, base_dark_oklch):
        """Generate card background for dark theme with neutral hue"""
        return np.array([0.21, 0.006, 285.885])  # Dark card background
    
    def adjust_primary_for_dark(self, primary_oklch):
        """Adjust primary color for dark theme"""
        l, c, h = primary_oklch
        return np.array([0.541, 0.281, h])

# Test the converter
if __name__ == "__main__":
    converter = ColorConverter()
    converter.test_conversion()






