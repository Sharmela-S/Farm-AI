/**
 * API Communication Module
 * Handles all backend API calls
 */

const API = {
    baseURL: window.location.origin,
    
    /**
     * Check API health status
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/api/health`);
            const data = await response.json();
            console.log('✅ API Health:', data);
            return data;
        } catch (error) {
            console.error('❌ API Health Check Failed:', error);
            return { status: 'error', message: error.message };
        }
    },

    /**
     * Analyze soil image and get crop recommendations
     * @param {File} imageFile - The soil image file
     * @param {Object} farmData - Farm details (location, season, etc.)
     */
    async analyzeSoil(imageFile, farmData) {
        try {
            // Create FormData object
            const formData = new FormData();
            formData.append('soil_image', imageFile);
            formData.append('location', farmData.location);
            formData.append('season', farmData.season);
            formData.append('temperature', farmData.temperature);
            formData.append('rainfall', farmData.rainfall);
            formData.append('humidity', farmData.humidity);
            
            if (farmData.previousCrop) {
                formData.append('previous_crop', farmData.previousCrop);
            }

            console.log('📤 Sending analysis request...');
            console.log('📸 Image:', imageFile.name);
            console.log('📍 Location:', farmData.location);

            // Make API call
            const response = await fetch(`${this.baseURL}/api/analyze`, {
                method: 'POST',
                body: formData
            });

            // Check if response is ok
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Analysis failed');
            }

            const data = await response.json();
            console.log('✅ Analysis complete:', data);
            return data;

        } catch (error) {
            console.error('❌ Analysis Error:', error);
            throw error;
        }
    },

    /**
     * Validate image file
     * @param {File} file - Image file to validate
     */
    validateImage(file) {
        const maxSize = 16 * 1024 * 1024; // 16MB
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp'];

        if (!file) {
            return { valid: false, error: 'No file selected' };
        }

        if (!allowedTypes.includes(file.type)) {
            return { valid: false, error: 'Invalid file type. Please upload JPG, PNG, or GIF' };
        }

        if (file.size > maxSize) {
            return { valid: false, error: 'File too large. Maximum size is 16MB' };
        }

        return { valid: true };
    },

    /**
     * Format error message for display
     * @param {Error} error - Error object
     */
    formatError(error) {
        if (error.message) {
            return error.message;
        }
        return 'An unexpected error occurred. Please try again.';
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}