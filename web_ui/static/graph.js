document.addEventListener('DOMContentLoaded', async function () {
    let lineGraph;  // Chart.js instance
    const ctx = document.getElementById('main-dash').getContext('2d');
    let deviceDataMap = {};
    let currentSelectedDevice = '';

    // Function to safely destroy any existing chart on the canvas
    function destroyExistingChart() {
        const existingChart = Chart.getChart(ctx);
        if (existingChart) {
            existingChart.destroy();
        }
        
        if (lineGraph) {
            lineGraph.destroy();
            lineGraph = null;
        }
    }

    // Normalization function
    function normalizeArray(values) {
        const min = Math.min(...values);
        const max = Math.max(...values);
        const range = max - min;
        
        if (range === 0) return values.map(() => 0);
        return values.map(value => (value - min) / range);
    }

    // Fetch sensor data and initialize the chart
    try {
        const response = await fetch('api/sensor_data');
        if (!response.ok) {
            throw new Error(`Error fetching data: HTTP status ${response.status}`);
        }

        const rawData = await response.json();
        deviceDataMap = transformData(rawData);
        populateDeviceDropdown(deviceDataMap);

        // Update graph on device selection change
        document.getElementById('device-selector').addEventListener('change', function () {
            console.log('Device changed to:', this.value);
            currentSelectedDevice = this.value;
            updateChart();
        });

        // Update graph on normalize checkbox change
        document.getElementById('normalize-data').addEventListener('change', function () {
            console.log('Normalize changed to:', this.checked);
            updateChart();
        });

    } catch (error) {
        console.error('Error:', error);
    }

    // Initial toggle for graph labels
    toggleGraphLabels();
    // Listen to window resize events
    window.addEventListener('resize', toggleGraphLabels);

    function transformData(rawData) {
        const deviceDataMap = {};
        rawData.forEach(entry => {
            const mac = entry.mac_address;
            if (!deviceDataMap[mac]) {
                deviceDataMap[mac] = [];
            }
            deviceDataMap[mac].push({
                Timestamp: new Date(entry.timestamp),
                Temperature: entry.temperature,
                Light: entry.light,
                Moisture: entry.moisture,
                Conductivity: entry.conductivity,
            });
        });
        console.log('Device Data Map:', deviceDataMap);
        return deviceDataMap;
    }
    
    // Populate the dropdown with device options
    function populateDeviceDropdown(deviceDataMap) {
        const dropdown = document.getElementById('device-selector');
        dropdown.innerHTML = Object.keys(deviceDataMap)
            .map(mac => `<option value="${mac}">${mac}</option>`)
            .join('');
        
        // Set initial device and trigger change
        if (dropdown.options.length > 0) {
            currentSelectedDevice = dropdown.value;
            dropdown.dispatchEvent(new Event('change'));
        }
    }

    // Update chart with current settings
    function updateChart() {
        if (!currentSelectedDevice || !deviceDataMap[currentSelectedDevice]) {
            return;
        }

        destroyExistingChart();
        
        const isNormalized = document.getElementById('normalize-data').checked;
        lineGraph = createLineGraph(ctx, deviceDataMap[currentSelectedDevice], isNormalized);
    }
    
    // Create a line graph using Chart.js
    function createLineGraph(ctx, deviceData, normalize = false) {
        const chartData = getChartData(deviceData, normalize);
        return new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    x: { 
                        reverse: false,
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: normalize ? 'Normalized Value (0-1)' : 'Sensor Value'
                        }
                    },
                },
            },
        });
    }

    // Extract relevant chart data from device data
    function getChartData(deviceData, normalize = false) {
        const timestamps = deviceData.map(item => item.Timestamp);
        const xAxisLabels = timestamps.map(ts => ts.toISOString().slice(0, 10));

        let temperatureData = deviceData.map(item => item.Temperature);
        let lightData = deviceData.map(item => item.Light);
        let moistureData = deviceData.map(item => item.Moisture);
        let conductivityData = deviceData.map(item => item.Conductivity);

        // Apply normalization if requested
        if (normalize) {
            temperatureData = normalizeArray(temperatureData);
            lightData = normalizeArray(lightData);
            moistureData = normalizeArray(moistureData);
            conductivityData = normalizeArray(conductivityData);
        }

        const suffix = normalize ? ' (Normalized)' : '';
        const units = normalize ? '' : ' (°C|lux|%|µS/cm)';

        return {
            labels: xAxisLabels,
            datasets: [
                createDataset(`Temperature${suffix}`, 'rgba(255, 165, 0, 0.75)', temperatureData),
                createDataset(`Light${suffix}`, 'rgba(0, 200, 0, 0.75)', lightData),
                createDataset(`Moisture${suffix}`, 'rgba(0, 0, 200, 0.75)', moistureData),
                createDataset(`Conductivity${suffix}`, 'rgba(200, 0, 0, 0.75)', conductivityData),
            ]
        };
    }

    // Helper function to create dataset
    function createDataset(label, color, data) {
        return {
            label,
            backgroundColor: color,
            borderColor: color,
            data,
            tension: 0.1
        };
    }

    // Toggle graph labels based on window width
    function toggleGraphLabels() {
        if (lineGraph) {
            const isMobile = window.innerWidth < 768;
            lineGraph.options.scales.x.display = !isMobile;
            lineGraph.options.scales.y.display = !isMobile;
            lineGraph.update();
        }
    }

    // Clean up when page is about to unload
    window.addEventListener('beforeunload', function() {
        destroyExistingChart();
    });
});