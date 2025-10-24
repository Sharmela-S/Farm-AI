"""
Utility functions for AI Crop Recommendation System
"""

import os
from PIL import Image
import numpy as np
from datetime import datetime

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, upload_folder):
    """Save uploaded file with timestamp"""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"soil_{timestamp}_{file.filename}"
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    return filepath

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image for analysis"""
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img)
    return img_array

def calculate_color_features(img_array):
    """Calculate color-based features from image"""
    # Average RGB values
    avg_color = img_array.mean(axis=(0, 1))
    r, g, b = avg_color[:3]
    
    # Brightness
    brightness = (r + g + b) / 3
    
    # Color variance (texture indicator)
    r_variance = np.var(img_array[:, :, 0])
    g_variance = np.var(img_array[:, :, 1])
    b_variance = np.var(img_array[:, :, 2])
    total_variance = r_variance + g_variance + b_variance
    
    # Color ratios
    red_dominance = r / (r + g + b) if (r + g + b) > 0 else 0
    green_dominance = g / (r + g + b) if (r + g + b) > 0 else 0
    blue_dominance = b / (r + g + b) if (r + g + b) > 0 else 0
    
    return {
        'r': float(r),
        'g': float(g),
        'b': float(b),
        'brightness': float(brightness),
        'variance': float(total_variance),
        'red_dominance': float(red_dominance),
        'green_dominance': float(green_dominance),
        'blue_dominance': float(blue_dominance)
    }

def get_crop_varieties(crop_name):
    """Get recommended varieties for a crop"""
    varieties = {
        'Rice': ['IR64', 'Basmati', 'Sona Masuri', 'Swarna', 'Pusa Basmati'],
        'Wheat': ['HD2967', 'PBW343', 'WH1105', 'Lok1', 'Sharbati'],
        'Cotton': ['Bt Cotton', 'Hybrid-6', 'Suraj', 'MCU5', 'Bunny Hybrid'],
        'Maize': ['DHM121', 'HQPM1', 'Vivek Hybrid', 'Sweet Corn', 'DHM-117'],
        'Sugarcane': ['Co86032', 'Co0238', 'CoJ88', 'Co419', 'CoLk-8102'],
        'Groundnut': ['TMV-2', 'JL-24', 'TAG-24', 'Kadiri-6', 'Kadiri-9'],
        'Soybean': ['JS-335', 'JS-9305', 'MACS-450', 'Pusa-16'],
        'Bajra': ['HHB-67', 'Pusa-322', 'RHB-121', 'GHB-558'],
        'Jowar': ['CSH-16', 'Maldandi', 'CSV-15', 'Pusa-9'],
        'Ragi': ['GPU-28', 'ML-365', 'VL-149', 'PR-202']
    }
    return varieties.get(crop_name, ['Local Variety', 'Hybrid Variety', 'Improved Variety'])

def calculate_fertilizer_requirement(soil_type, crop_name, area_hectares=1):
    """Calculate fertilizer requirements"""
    # Base NPK requirements per hectare for different crops
    npk_base = {
        'Rice': {'N': 120, 'P': 60, 'K': 40},
        'Wheat': {'N': 120, 'P': 60, 'K': 40},
        'Cotton': {'N': 150, 'P': 75, 'K': 75},
        'Maize': {'N': 120, 'P': 60, 'K': 40},
        'Sugarcane': {'N': 250, 'P': 115, 'K': 115}
    }
    
    requirements = npk_base.get(crop_name, {'N': 100, 'P': 50, 'K': 50})
    
    return {
        'nitrogen': f"{requirements['N'] * area_hectares} kg",
        'phosphorus': f"{requirements['P'] * area_hectares} kg",
        'potassium': f"{requirements['K'] * area_hectares} kg",
        'organic': f"{10 * area_hectares} tons of farmyard manure"
    }

def calculate_irrigation_requirement(crop_name, soil_type, season):
    """Calculate irrigation requirements"""
    water_needs = {
        'Rice': 1500,
        'Wheat': 550,
        'Cotton': 900,
        'Maize': 650,
        'Sugarcane': 2000,
        'Groundnut': 600
    }
    
    base_water = water_needs.get(crop_name, 700)
    
    # Soil adjustment
    soil_multiplier = {
        'Sandy Soil': 1.3,
        'Clay Soil': 0.9,
        'Loamy Soil': 1.0,
        'Silty Soil': 1.1
    }
    
    adjusted_water = base_water * soil_multiplier.get(soil_type, 1.0)
    
    return {
        'total_water_mm': round(adjusted_water, 2),
        'frequency': get_irrigation_frequency(soil_type),
        'method': get_irrigation_method(crop_name)
    }

def get_irrigation_frequency(soil_type):
    """Get irrigation frequency based on soil type"""
    frequency_map = {
        'Sandy Soil': 'Every 5-7 days',
        'Clay Soil': 'Every 10-15 days',
        'Loamy Soil': 'Every 7-10 days',
        'Silty Soil': 'Every 8-12 days'
    }
    return frequency_map.get(soil_type, 'Every 7-10 days')

def get_irrigation_method(crop_name):
    """Recommend irrigation method based on crop"""
    if crop_name in ['Cotton', 'Groundnut', 'Vegetables']:
        return 'Drip Irrigation (90% efficiency)'
    elif crop_name in ['Wheat', 'Maize']:
        return 'Sprinkler Irrigation (75% efficiency)'
    elif crop_name == 'Rice':
        return 'Flood Irrigation (40% efficiency)'
    else:
        return 'Drip or Sprinkler Irrigation'

def estimate_yield(crop_name, soil_type, rainfall):
    """Estimate crop yield"""
    base_yields = {
        'Rice': 4.5,
        'Wheat': 3.2,
        'Cotton': 2.8,
        'Maize': 3.8,
        'Sugarcane': 70.0,
        'Groundnut': 2.2
    }
    
    base_yield = base_yields.get(crop_name, 3.0)
    
    # Adjust based on rainfall
    if rainfall < 500:
        base_yield *= 0.8
    elif rainfall > 1500:
        base_yield *= 0.9
    
    return round(base_yield, 1)

def calculate_roi(crop_name, area_hectares):
    """Calculate Return on Investment"""
    costs_per_ha = {
        'Rice': 35000,
        'Wheat': 31000,
        'Cotton': 46000,
        'Maize': 32000,
        'Sugarcane': 80000
    }
    
    revenue_per_ha = {
        'Rice': 112500,
        'Wheat': 70400,
        'Cotton': 182000,
        'Maize': 68400,
        'Sugarcane': 240000
    }
    
    total_cost = costs_per_ha.get(crop_name, 35000) * area_hectares
    expected_revenue = revenue_per_ha.get(crop_name, 100000) * area_hectares
    net_profit = expected_revenue - total_cost
    roi_percentage = (net_profit / total_cost) * 100 if total_cost > 0 else 0
    
    return {
        'total_investment': total_cost,
        'expected_revenue': expected_revenue,
        'net_profit': net_profit,
        'roi_percentage': round(roi_percentage, 2)
    }

def format_response(data):
    """Format API response"""
    return {
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'data': data
    }

def format_error(error_message, status_code=400):
    """Format error response"""
    return {
        'status': 'error',
        'message': error_message,
        'timestamp': datetime.now().isoformat()
    }, status_code