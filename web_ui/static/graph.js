document.addEventListener('DOMContentLoaded', async function () {
    let lineGraph;  // Chart.js instance
    const ctx = document.getElementById('main-dash');

    // Fetch sensor data and initialize the chart
    try {
        const response = await fetch('api/sensor_data');
        if (!response.ok) {
            throw new Error(`Error fetching data: HTTP status ${response.status}`);
        }

        const rawData = await response.json();
        const deviceDataMap = transformData(rawData);
        populateDeviceDropdown(deviceDataMap);

        // Initial graph setup
        const initialMac = Object.keys(deviceDataMap)[0];
        if (initialMac) {
            lineGraph = createLineGraph(ctx, deviceDataMap[initialMac]);
        }

        // Update graph on device selection change
        document.getElementById('device-selector').addEventListener('change', function () {
            if (lineGraph) {
                lineGraph.destroy();  // Destroy the existing chart instance
            }
            lineGraph = createLineGraph(ctx, deviceDataMap[this.value]);
        });
    } catch (error) {
        console.error('Error:', error);
    }

    // Initial toggle for graph labels
    toggleGraphLabels();
    // Listen to window resize events
    window.addEventListener('resize', toggleGraphLabels);

    // Transform raw data into a structured format
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
        return deviceDataMap;
    }

    // Populate the dropdown with device options
    function populateDeviceDropdown(deviceDataMap) {
        const dropdown = document.getElementById('device-selector');
        dropdown.innerHTML = Object.keys(deviceDataMap)
            .map(mac => `<option value="${mac}">${mac}</option>`)
            .join('');
        dropdown.dispatchEvent(new Event('change')); // Trigger change event to show the initial data
    }

    // Create a line graph using Chart.js
    function createLineGraph(ctx, deviceData) {
        const chartData = getChartData(deviceData);
        return new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                scales: {
                    x: { reverse: false }, // Display X-axis normally
                    y: { display: true },  // Show Y-axis labels
                },
            },
        });
    }

    // Extract relevant chart data from device data
    function getChartData(deviceData) {
        const timestamps = deviceData.map(item => item.Timestamp);
        const xAxisLabels = timestamps.map(ts => ts.toISOString().slice(0, 10));

        return {
            labels: xAxisLabels,
            datasets: [
                createDataset('Temperature', 'rgba(255, 165, 0, 0.75)', deviceData.map(item => item.Temperature)),
                createDataset('Light', 'rgba(0, 200, 0, 0.75)', deviceData.map(item => item.Light)),
                createDataset('Moisture', 'rgba(0, 0, 200, 0.75)', deviceData.map(item => item.Moisture)),
                createDataset('Conductivity', 'rgba(200, 0, 0, 0.75)', deviceData.map(item => item.Conductivity)),
            ],
        };
    }

    // Helper function to create dataset
    function createDataset(label, color, data) {
        return {
            label,
            backgroundColor: color,
            borderColor: color,
            data,
        };
    }

    // Toggle graph labels based on window width
    function toggleGraphLabels() {
        if (lineGraph) {
            const isMobile = window.innerWidth < 768;
            lineGraph.options.scales.x.display = !isMobile; // Show/hide X-axis labels
            lineGraph.options.scales.y.display = !isMobile; // Show/hide Y-axis labels
            lineGraph.update(); // Update the chart to reflect changes
        }
    }
});
