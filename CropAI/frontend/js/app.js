/**
 * Main Application Logic
 * Handles UI interactions and application flow
 */

// Global state
let selectedImage = null;
let analysisResults = null;

// DOM Elements
const elements = {
    // Steps
    step1: document.getElementById('step-1'),
    step2: document.getElementById('step-2'),
    step3: document.getElementById('step-3'),
    stepLoading: document.getElementById('step-loading'),
    
    // Step indicators
    stepIndicator1: document.getElementById('step-indicator-1'),
    stepIndicator2: document.getElementById('step-indicator-2'),
    stepIndicator3: document.getElementById('step-indicator-3'),
    
    // Upload elements
    uploadBox: document.getElementById('upload-box'),
    soilImageInput: document.getElementById('soil-image'),
    uploadContent: document.getElementById('upload-content'),
    imagePreview: document.getElementById('image-preview'),
    previewImg: document.getElementById('preview-img'),
    removeImageBtn: document.getElementById('remove-image'),
    nextToStep2Btn: document.getElementById('next-to-step-2'),
    
    // Form elements
    form: document.getElementById('farm-details-form'),
    locationInput: document.getElementById('location'),
    seasonInput: document.getElementById('season'),
    temperatureInput: document.getElementById('temperature'),
    rainfallInput: document.getElementById('rainfall'),
    humidityInput: document.getElementById('humidity'),
    previousCropInput: document.getElementById('previous-crop'),
    
    // Navigation buttons
    backToStep1Btn: document.getElementById('back-to-step-1'),
    analyzeBtn: document.getElementById('analyze-button'),
    analyzeAnotherBtn: document.getElementById('analyze-another'),
    downloadReportBtn: document.getElementById('download-report'),
    
    // Results container
    resultsContainer: document.getElementById('results-container')
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌾 AI Crop Recommendation System initialized');
    initializeEventListeners();
    checkAPIHealth();
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // Upload box click
    elements.uploadBox.addEventListener('click', () => {
        elements.soilImageInput.click();
    });
    
    // File input change
    elements.soilImageInput.addEventListener('change', handleImageUpload);
    
    // Remove image button
    elements.removeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        removeImage();
    });
    
    // Navigation buttons
    elements.nextToStep2Btn.addEventListener('click', () => showStep(2));
    elements.backToStep1Btn.addEventListener('click', () => showStep(1));
    elements.analyzeBtn.addEventListener('click', analyzeForm);
    elements.analyzeAnotherBtn.addEventListener('click', resetApplication);
    elements.downloadReportBtn.addEventListener('click', downloadReport);
    
    // Form validation
    elements.form.addEventListener('input', validateForm);
    
    // Drag and drop
    elements.uploadBox.addEventListener('dragover', handleDragOver);
    elements.uploadBox.addEventListener('drop', handleDrop);
}

/**
 * Check API health status
 */
async function checkAPIHealth() {
    try {
        const health = await API.checkHealth();
        if (health.status === 'healthy') {
            console.log('✅ Backend connected successfully');
        }
    } catch (error) {
        console.error('⚠️ Backend not reachable:', error);
        showNotification('Warning: Backend server not connected', 'warning');
    }
}

/**
 * Handle image upload
 */
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validate image
    const validation = API.validateImage(file);
    if (!validation.valid) {
        showNotification(validation.error, 'error');
        return;
    }
    
    // Store file
    selectedImage = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        elements.previewImg.src = e.target.result;
        elements.uploadContent.hidden = true;
        elements.imagePreview.hidden = false;
        elements.nextToStep2Btn.disabled = false;
        
        showNotification('✅ Image uploaded successfully!', 'success');
    };
    reader.readAsDataURL(file);
}

/**
 * Remove uploaded image
 */
function removeImage() {
    selectedImage = null;
    elements.soilImageInput.value = '';
    elements.uploadContent.hidden = false;
    elements.imagePreview.hidden = true;
    elements.nextToStep2Btn.disabled = true;
}

/**
 * Handle drag over event
 */
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadBox.style.borderColor = 'var(--primary-color)';
    elements.uploadBox.style.background = 'rgba(34, 197, 94, 0.05)';
}

/**
 * Handle drop event
 */
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadBox.style.borderColor = '';
    elements.uploadBox.style.background = '';
    
    const file = e.dataTransfer.files[0];
    if (file) {
        elements.soilImageInput.files = e.dataTransfer.files;
        handleImageUpload({ target: elements.soilImageInput });
    }
}

/**
 * Validate form
 */
function validateForm() {
    const isValid = 
        elements.locationInput.value.trim() !== '' &&
        elements.seasonInput.value !== '' &&
        elements.temperatureInput.value !== '' &&
        elements.rainfallInput.value !== '' &&
        elements.humidityInput.value !== '';
    
    elements.analyzeBtn.disabled = !isValid;
    return isValid;
}

/**
 * Show specific step
 */
function showStep(stepNumber) {
    // Hide all steps
    elements.step1.hidden = true;
    elements.step2.hidden = true;
    elements.step3.hidden = true;
    elements.stepLoading.hidden = true;
    
    // Remove active class from all indicators
    elements.stepIndicator1.classList.remove('active');
    elements.stepIndicator2.classList.remove('active');
    elements.stepIndicator3.classList.remove('active');
    
    // Show requested step
    if (stepNumber === 1) {
        elements.step1.hidden = false;
        elements.stepIndicator1.classList.add('active');
    } else if (stepNumber === 2) {
        elements.step2.hidden = false;
        elements.stepIndicator2.classList.add('active');
    } else if (stepNumber === 3) {
        elements.step3.hidden = false;
        elements.stepIndicator3.classList.add('active');
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Analyze form and get recommendations
 */
async function analyzeForm() {
    if (!validateForm()) {
        showNotification('Please fill all required fields', 'error');
        return;
    }
    
    if (!selectedImage) {
        showNotification('Please upload a soil image', 'error');
        return;
    }
    
    // Show loading
    elements.step2.hidden = true;
    elements.stepLoading.hidden = false;
    
    // Prepare form data
    const farmData = {
        location: elements.locationInput.value.trim(),
        season: elements.seasonInput.value,
        temperature: parseFloat(elements.temperatureInput.value),
        rainfall: parseFloat(elements.rainfallInput.value),
        humidity: parseFloat(elements.humidityInput.value),
        previousCrop: elements.previousCropInput.value.trim()
    };
    
    try {
        // Call API
        const results = await API.analyzeSoil(selectedImage, farmData);
        
        // Store results
        analysisResults = results;
        
        // Display results
        displayResults(results);
        
        // Show results step
        showStep(3);
        
    } catch (error) {
        console.error('Analysis failed:', error);
        showNotification(API.formatError(error), 'error');
        showStep(2);
    }
}

/**
 * Display analysis results
 */
function displayResults(data) {
    const container = elements.resultsContainer;
    container.innerHTML = '';
    
    // Soil Analysis Card
    const soilCard = createSoilAnalysisCard(data.soil_analysis);
    container.appendChild(soilCard);
    
    // Crops Recommendation Card
    const cropsCard = createCropsCard(data.recommended_crops);
    container.appendChild(cropsCard);
    
    // Fertilizer & Irrigation Card
    const fertIrrigCard = createFertilizerIrrigationCard(data.fertilizer, data.irrigation);
    container.appendChild(fertIrrigCard);
    
    // Tips Card
    const tipsCard = createTipsCard(data.tips);
    container.appendChild(tipsCard);
}

/**
 * Create soil analysis card
 */
function createSoilAnalysisCard(soilData) {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.innerHTML = `
        <h3>🔬 Soil Analysis Result</h3>
        <div class="soil-analysis-box">
            <div class="soil-type">${soilData.soil_type}</div>
            <div class="confidence">AI Confidence: ${soilData.confidence}%</div>
            <p style="margin-top: 1rem; color: var(--text-light);">
                Analysis based on color, texture, and pattern recognition
            </p>
        </div>
    `;
    return card;
}

/**
 * Create crops recommendation card
 */
function createCropsCard(crops) {
    const card = document.createElement('div');
    card.className = 'result-card';
    
    const cropsHTML = crops.map((crop, index) => `
        <div class="crop-card">
            <div class="crop-header">
                <div class="crop-name">${index + 1}. ${crop.name}</div>
                <div class="crop-score">${crop.suitability}%</div>
            </div>
            <div class="crop-details">
                <div class="crop-detail-item">
                    <strong>Yield:</strong>
                    <span>${crop.yield}</span>
                </div>
                <div class="crop-detail-item">
                    <strong>Duration:</strong>
                    <span>${crop.duration}</span>
                </div>
                <div class="crop-detail-item">
                    <strong>Profit:</strong>
                    <span>${crop.profit}</span>
                </div>
            </div>
        </div>
    `).join('');
    
    card.innerHTML = `
        <h3>🌾 Top Recommended Crops</h3>
        <div class="crops-grid">
            ${cropsHTML}
        </div>
    `;
    return card;
}

/**
 * Create fertilizer and irrigation card
 */
function createFertilizerIrrigationCard(fertilizer, irrigation) {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.innerHTML = `
        <h3>🧪 Fertilizer & Irrigation Plan</h3>
        <div class="info-grid">
            <div class="info-box">
                <h4>NPK Requirements</h4>
                <ul>
                    <li><strong>Nitrogen:</strong> ${fertilizer.nitrogen}</li>
                    <li><strong>Phosphorus:</strong> ${fertilizer.phosphorus}</li>
                    <li><strong>Potassium:</strong> ${fertilizer.potassium}</li>
                </ul>
                <p style="margin-top: 1rem; padding-top: 1rem; border-top: 2px solid var(--border-color);">
                    <strong>Organic:</strong> ${fertilizer.organic}
                </p>
            </div>
            <div class="info-box">
                <h4>💧 Irrigation Advisory</h4>
                <ul>
                    <li><strong>Frequency:</strong> ${irrigation.frequency}</li>
                    <li><strong>Method:</strong> ${irrigation.method}</li>
                    <li><strong>Water Need:</strong> ${irrigation.water_requirement}</li>
                </ul>
            </div>
        </div>
    `;
    return card;
}

/**
 * Create tips card
 */
function createTipsCard(tips) {
    const card = document.createElement('div');
    card.className = 'result-card';
    
    const tipsHTML = tips.map((tip, index) => `
        <li><strong>${index + 1}.</strong> ${tip}</li>
    `).join('');
    
    card.innerHTML = `
        <h3>💡 Expert Recommendations</h3>
        <ul class="tips-list">
            ${tipsHTML}
        </ul>
    `;
    return card;
}

/**
 * Download PDF report
 */
function downloadReport() {
    if (!analysisResults) {
        showNotification('No results to download', 'error');
        return;
    }
    
    // Create report window
    const reportWindow = window.open('', '_blank');
    const reportHTML = generateReportHTML(analysisResults);
    reportWindow.document.write(reportHTML);
    reportWindow.document.close();
    
    // Show print dialog after a short delay
    setTimeout(() => {
        reportWindow.print();
    }, 500);
    
    showNotification('✅ Report ready to download!', 'success');
}

/**
 * Generate HTML for PDF report
 */
function generateReportHTML(data) {
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crop Recommendation Report</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h1 { color: #22c55e; text-align: center; }
            .section { margin: 20px 0; padding: 15px; border: 2px solid #22c55e; border-radius: 10px; }
            .section h2 { color: #16a34a; margin-bottom: 10px; }
            .crop { background: #f0fdf4; padding: 10px; margin: 10px 0; border-radius: 8px; }
            @media print { button { display: none; } }
        </style>
    </head>
    <body>
        <h1>🌾 AI Crop Recommendation Report</h1>
        <p style="text-align: center;">Generated: ${new Date().toLocaleString()}</p>
        
        <div class="section">
            <h2>🔬 Soil Analysis</h2>
            <p><strong>Soil Type:</strong> ${data.soil_analysis.soil_type}</p>
            <p><strong>Confidence:</strong> ${data.soil_analysis.confidence}%</p>
        </div>
        
        <div class="section">
            <h2>🌾 Recommended Crops</h2>
            ${data.recommended_crops.map((crop, i) => `
                <div class="crop">
                    <strong>${i+1}. ${crop.name}</strong> (${crop.suitability}% match)<br>
                    Yield: ${crop.yield} | Duration: ${crop.duration}
                </div>
            `).join('')}
        </div>
        
        <div class="section">
            <h2>🧪 Fertilizer Plan</h2>
            <p>Nitrogen: ${data.fertilizer.nitrogen}</p>
            <p>Phosphorus: ${data.fertilizer.phosphorus}</p>
            <p>Potassium: ${data.fertilizer.potassium}</p>
        </div>
        
        <div class="section">
            <h2>💡 Expert Tips</h2>
            <ul>
                ${data.tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
        
        <button onclick="window.print()" style="background: #22c55e; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; margin: 20px auto; display: block;">
            📥 Download as PDF
        </button>
    </body>
    </html>
    `;
}

/**
 * Reset application to start over
 */
function resetApplication() {
    // Clear state
    selectedImage = null;
    analysisResults = null;
    
    // Reset form
    elements.form.reset();
    elements.soilImageInput.value = '';
    
    // Reset upload box
    elements.uploadContent.hidden = false;
    elements.imagePreview.hidden = true;
    elements.nextToStep2Btn.disabled = true;
    
    // Go back to step 1
    showStep(1);
    
    showNotification('Ready for new analysis', 'info');
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        font-weight: 600;
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Smooth scroll to analyze section
 */
function scrollToAnalyze() {
    document.getElementById('analyze').scrollIntoView({ behavior: 'smooth' });
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

console.log('✅ Application initialized successfully!');