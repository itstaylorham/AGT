// normalize.js - Data normalization and processing for Agrotech sensor data

/**
 * Fetches sensor data from the API
 * @returns {Promise<Array>} Array of sensor data records
 */
async function fetchSensorData() {
    try {
        const response = await fetch('/api/sensor_data');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching sensor data:', error);
        return [];
    }
}

/**
 * Processes raw sensor data into a format suitable for visualization
 * @param {Array} rawData - Raw sensor data from API
 * @returns {Object} Processed data with separate arrays for each metric
 */
function processSensorData(rawData) {
    return {
        timestamps: rawData.map(d => new Date(d.timestamp)),
        macAddresses: rawData.map(d => d.mac_address),
        temperature: rawData.map(d => parseFloat(d.temperature)),
        moisture: rawData.map(d => parseFloat(d.moisture)),
        light: rawData.map(d => parseFloat(d.light)),
        conductivity: rawData.map(d => parseFloat(d.conductivity))
    };
}

/**
 * Normalizes an array of values using min-max normalization
 * @param {Array<number>} values - Array of numerical values to normalize
 * @returns {Array<number>} Normalized values between 0 and 1
 */
function normalizeArray(values) {
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min;
    
    if (range === 0) return values.map(() => 0);
    return values.map(value => (value - min) / range);
}

/**
 * Normalizes processed sensor data
 * @param {Object} processedData - Processed sensor data object
 * @param {Object} options - Normalization options
 * @returns {Object} Normalized sensor data
 */
function normalizeSensorData(processedData, options = {}) {
    const {
        normalizeTemperature = true,
        normalizeMoisture = true,
        normalizeLight = true,
        normalizeConductivity = true
    } = options;

    const result = { ...processedData };

    if (normalizeTemperature) {
        result.temperature = normalizeArray(processedData.temperature);
    }
    if (normalizeMoisture) {
        result.moisture = normalizeArray(processedData.moisture);
    }
    if (normalizeLight) {
        result.light = normalizeArray(processedData.light);
    }
    if (normalizeConductivity) {
        result.conductivity = normalizeArray(processedData.conductivity);
    }

    return result;
}

/**
 * Updates the chart with current sensor data
 * @param {Object} chartInstance - Chart.js instance
 * @param {boolean} normalized - Whether to normalize the data
 */
async function updateChart(chartInstance, normalized = false) {
    const rawData = await fetchSensorData();
    const processedData = processSensorData(rawData);
    
    const displayData = normalized ? 
        normalizeSensorData(processedData) : 
        processedData;

    chartInstance.data.labels = displayData.timestamps.map(t => 
        t.toLocaleString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            hour: '2-digit', 
            minute: '2-digit' 
        })
    );

    chartInstance.data.datasets = [
        {
            label: 'Temperature' + (normalized ? ' (Normalized)' : ' (°C)'),
            data: displayData.temperature,
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1
        },
        {
            label: 'Moisture' + (normalized ? ' (Normalized)' : ' (%)'),
            data: displayData.moisture,
            borderColor: 'rgb(54, 162, 235)',
            tension: 0.1
        },
        {
            label: 'Light' + (normalized ? ' (Normalized)' : ' (lux)'),
            data: displayData.light,
            borderColor: 'rgb(255, 206, 86)',
            tension: 0.1
        },
        {
            label: 'Conductivity' + (normalized ? ' (Normalized)' : ' (µS/cm)'),
            data: displayData.conductivity,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }
    ];

    chartInstance.update();
}

// Initialize chart and set up event listeners
document.addEventListener('DOMContentLoaded', async () => {
    const ctx = document.getElementById('main-dash').getContext('2d');
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        }
    });

    // Initial chart update
    await updateChart(chart, false);

    // Set up normalize checkbox listener
    const normalizeCheckbox = document.getElementById('normalize-data');
    normalizeCheckbox.addEventListener('change', async (e) => {
        await updateChart(chart, e.target.checked);
    });

    // Set up auto-refresh every 5 minutes
    setInterval(async () => {
        await updateChart(chart, normalizeCheckbox.checked);
    }, 5 * 60 * 1000);
});

export {
    fetchSensorData,
    processSensorData,
    normalizeSensorData,
    updateChart
};