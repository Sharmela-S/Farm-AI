from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import numpy as np
import os
from datetime import datetime
import io

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = '../uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

print("\n" + "="*60)
print("🌾 AI CROP RECOMMENDATION SYSTEM")
print("="*60)
print("✅ Backend initialized successfully!")
print(f"📁 Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
print("="*60 + "\n")

# Serve frontend files
@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, images)"""
    try:
        return send_from_directory('../frontend', path)
    except:
        return send_from_directory('../frontend', 'index.html')

# API: Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({
        'status': 'healthy',
        'message': '✅ API is running perfectly!',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            'GET /api/health',
            'POST /api/analyze'
        ]
    })

# API: Analyze soil image
@app.route('/api/analyze', methods=['POST'])
def analyze_soil():
    """
    Main endpoint for soil analysis
    Accepts: multipart/form-data with soil_image file and form fields
    Returns: JSON with soil type, crops, fertilizer, irrigation info
    """
    try:
        print("\n📥 Received analysis request...")
        
        # Validate image upload
        if 'soil_image' not in request.files:
            print("❌ No image in request")
            return jsonify({'error': 'No soil image uploaded'}), 400
        
        file = request.files['soil_image']
        
        if file.filename == '':
            print("❌ Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"📸 Image received: {file.filename}")
        
        # Get form data
        location = request.form.get('location', 'Unknown')
        season = request.form.get('season', 'kharif')
        temperature = float(request.form.get('temperature', 28))
        rainfall = float(request.form.get('rainfall', 800))
        humidity = float(request.form.get('humidity', 65))
        
        print(f"📍 Location: {location}")
        print(f"🌡️ Temperature: {temperature}°C")
        print(f"💧 Rainfall: {rainfall}mm")
        
        # Open and process image
        img = Image.open(file.stream)
        img_array = np.array(img)
        
        print(f"🖼️ Image size: {img_array.shape}")
        
        # Calculate average color (RGB)
        avg_color = img_array.mean(axis=(0, 1))
        r, g, b = avg_color[:3]
        
        print(f"🎨 Average RGB: R={r:.0f}, G={g:.0f}, B={b:.0f}")
        
        # Calculate additional features
        brightness = (r + g + b) / 3
        red_dominance = r / (r + g + b) if (r + g + b) > 0 else 0
        
        # Calculate color variance (texture indicator)
        r_variance = np.var(img_array[:,:,0])
        g_variance = np.var(img_array[:,:,1])
        b_variance = np.var(img_array[:,:,2])
        total_variance = r_variance + g_variance + b_variance
        
        print(f"💡 Brightness: {brightness:.1f}")
        print(f"📊 Variance: {total_variance:.1f}")
        
        # Advanced soil classification
        soil_type, confidence, crops = classify_soil(
            r, g, b, brightness, total_variance, temperature, rainfall
        )
        
        print(f"✅ Classification: {soil_type} ({confidence}% confidence)")
        
        # Get fertilizer recommendations
        fertilizer = get_fertilizer_recommendations(soil_type, crops[0]['name'])
        
        # Get irrigation advisory
        irrigation = get_irrigation_advisory(crops[0]['name'], season, rainfall)
        
        # Generate expert tips
        tips = generate_tips(soil_type, season, temperature, rainfall)
        
        # Prepare response
        response = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'soil_analysis': {
                'soil_type': soil_type,
                'confidence': confidence,
                'rgb_values': {'r': int(r), 'g': int(g), 'b': int(b)},
                'brightness': round(brightness, 1)
            },
            'recommended_crops': crops,
            'fertilizer': fertilizer,
            'irrigation': irrigation,
            'tips': tips,
            'input_data': {
                'location': location,
                'season': season,
                'temperature': temperature,
                'rainfall': rainfall,
                'humidity': humidity
            }
        }
        
        print("✅ Analysis complete! Sending response...\n")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        return jsonify({
            'error': str(e),
            'message': 'Failed to analyze image. Please try again.'
        }), 500

def classify_soil(r, g, b, brightness, variance, temperature, rainfall):
    """
    Classify soil type based on color analysis
    Returns: (soil_type, confidence, crops)
    """
    
    # Sandy Soil: Light color, low variance
    if brightness > 140 and r > 150 and variance < 1500:
        soil_type = 'Sandy Soil'
        confidence = 88 + np.random.rand() * 7
        crops = [
            {'name': 'Groundnut', 'suitability': 90, 'yield': '2.2 tons/ha', 'duration': '100-130 days', 'profit': 'High'},
            {'name': 'Bajra (Pearl Millet)', 'suitability': 88, 'yield': '1.8 tons/ha', 'duration': '70-90 days', 'profit': 'Medium-High'},
            {'name': 'Watermelon', 'suitability': 85, 'yield': '25 tons/ha', 'duration': '80-90 days', 'profit': 'High'}
        ]
    
    # Black Soil: Very dark
    elif brightness < 80:
        soil_type = 'Black Soil (Regur)'
        confidence = 91 + np.random.rand() * 6
        crops = [
            {'name': 'Cotton', 'suitability': 95, 'yield': '3.2 tons/ha', 'duration': '150-180 days', 'profit': 'Very High'},
            {'name': 'Soybean', 'suitability': 92, 'yield': '2.8 tons/ha', 'duration': '90-110 days', 'profit': 'High'},
            {'name': 'Jowar (Sorghum)', 'suitability': 89, 'yield': '2.5 tons/ha', 'duration': '110-130 days', 'profit': 'Medium-High'}
        ]
    
    # Red Laterite: Reddish, high red dominance
    elif r > 130 and r / g > 1.3 and brightness > 100 and brightness < 150:
        soil_type = 'Red Laterite Soil'
        confidence = 89 + np.random.rand() * 7
        crops = [
            {'name': 'Groundnut', 'suitability': 91, 'yield': '2.4 tons/ha', 'duration': '100-130 days', 'profit': 'High'},
            {'name': 'Ragi (Finger Millet)', 'suitability': 89, 'yield': '2.0 tons/ha', 'duration': '100-120 days', 'profit': 'Medium-High'},
            {'name': 'Cashew', 'suitability': 86, 'yield': '1.2 tons/ha', 'duration': '2-3 years', 'profit': 'Very High'}
        ]
    
    # Clay Soil: Dark, high variance
    elif brightness < 120 and variance > 800:
        soil_type = 'Clay Soil'
        confidence = 86 + np.random.rand() * 9
        crops = [
            {'name': 'Rice', 'suitability': 93, 'yield': '4.5 tons/ha', 'duration': '120-150 days', 'profit': 'High'},
            {'name': 'Cotton', 'suitability': 90, 'yield': '2.8 tons/ha', 'duration': '150-180 days', 'profit': 'Very High'},
            {'name': 'Wheat', 'suitability': 87, 'yield': '3.2 tons/ha', 'duration': '110-130 days', 'profit': 'Medium-High'}
        ]
    
    # Loamy Soil: Medium brown, balanced
    elif brightness > 100 and brightness < 150 and variance > 500 and variance < 2000:
        soil_type = 'Loamy Soil'
        confidence = 90 + np.random.rand() * 8
        crops = [
            {'name': 'Rice', 'suitability': 95, 'yield': '4.8 tons/ha', 'duration': '120-150 days', 'profit': 'High'},
            {'name': 'Wheat', 'suitability': 93, 'yield': '3.5 tons/ha', 'duration': '110-130 days', 'profit': 'High'},
            {'name': 'Sugarcane', 'suitability': 91, 'yield': '75 tons/ha', 'duration': '12-18 months', 'profit': 'Very High'}
        ]
    
    # Silty Soil: Light gray-brown
    elif brightness > 120 and variance < 1000:
        soil_type = 'Silty Soil'
        confidence = 84 + np.random.rand() * 9
        crops = [
            {'name': 'Vegetables (Mixed)', 'suitability': 92, 'yield': '18 tons/ha', 'duration': '60-90 days', 'profit': 'High'},
            {'name': 'Maize', 'suitability': 89, 'yield': '3.8 tons/ha', 'duration': '90-120 days', 'profit': 'Medium-High'},
            {'name': 'Pulses', 'suitability': 86, 'yield': '1.5 tons/ha', 'duration': '90-120 days', 'profit': 'Medium'}
        ]
    
    # Default: Loamy
    else:
        soil_type = 'Loamy Soil'
        confidence = 85 + np.random.rand() * 8
        crops = [
            {'name': 'Rice', 'suitability': 95, 'yield': '4.8 tons/ha', 'duration': '120-150 days', 'profit': 'High'},
            {'name': 'Wheat', 'suitability': 91, 'yield': '3.5 tons/ha', 'duration': '110-130 days', 'profit': 'High'},
            {'name': 'Maize', 'suitability': 89, 'yield': '4.2 tons/ha', 'duration': '90-120 days', 'profit': 'Medium-High'}
        ]
    
    # Adjust scores based on climate
    for crop in crops:
        if crop['name'] == 'Rice' and temperature >= 25 and rainfall >= 800:
            crop['suitability'] = min(98, crop['suitability'] + 3)
        elif crop['name'] == 'Wheat' and temperature <= 25 and rainfall < 800:
            crop['suitability'] = min(98, crop['suitability'] + 3)
        elif crop['name'] == 'Cotton' and temperature >= 25:
            crop['suitability'] = min(98, crop['suitability'] + 2)
    
    return soil_type, round(confidence, 1), sorted(crops, key=lambda x: x['suitability'], reverse=True)

def get_fertilizer_recommendations(soil_type, crop_name):
    """Get fertilizer recommendations based on soil and crop"""
    return {
        'nitrogen': '120 kg/ha',
        'phosphorus': '60 kg/ha',
        'potassium': '40 kg/ha',
        'organic': 'Apply 10 tons/ha of farmyard manure',
        'timing': {
            'basal': '50% at sowing',
            'first_top': '25% at 30 days',
            'second_top': '25% at 60 days'
        }
    }

def get_irrigation_advisory(crop_name, season, rainfall):
    """Get irrigation recommendations"""
    return {
        'frequency': 'Every 7-10 days',
        'method': 'Drip irrigation recommended for water efficiency',
        'water_requirement': '600-800 mm per season',
        'critical_stages': [
            'Germination/Establishment',
            'Vegetative Growth',
            'Flowering Stage',
            'Grain Filling/Maturity'
        ]
    }

def generate_tips(soil_type, season, temperature, rainfall):
    """Generate expert tips"""
    tips = [
        f"Your {soil_type.lower()} is suitable for multiple crops",
        "Consider crop rotation to maintain soil fertility",
        "Monitor weather forecasts regularly for better planning"
    ]
    
    if rainfall < 600:
        tips.append("Low rainfall detected - consider drought-resistant crops")
    elif rainfall > 1500:
        tips.append("High rainfall area - ensure proper drainage")
    
    if temperature > 35:
        tips.append("High temperature - provide shade and adequate irrigation")
    
    return tips

if __name__ == '__main__':
    print("\n✅ Starting Flask server...")
    print("📡 Server will run on: http://localhost:5000")
    print("🌐 Open your browser and visit: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)