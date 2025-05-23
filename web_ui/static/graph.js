document.addEventListener('DOMContentLoaded', async function () {
    let lineGraph;  // Chart.js instance
    const ctx = document.getElementById('main-dash').getContext('2d');;

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
            console.log('Device changed to:', this.value);
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
        console.log('Device Data Map:', deviceDataMap); // ← moved inside
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
                    y: {
                        display: true,
                        ticks: {
                            callback: function (value, index, values) {
                                // Assuming value here is the index of the hour in uniqueHours
                                return chartData.yAxisLabels[value];
                            }
                        }
                    },
                },
            },
        });
    }

    // Extract relevant chart data from device data
    function getChartData(deviceData) {
        const timestamps = deviceData.map(item => item.Timestamp);
        const xAxisLabels = timestamps.map(ts => ts.toISOString().slice(0, 10));

        // Extract hours for Y-axis labels
        const hours = timestamps.map(timestamp => timestamp.getHours() + ':00');
        const uniqueHours = [...new Set(hours)];
        const yAxisLabels = uniqueHours.sort(); // Sort hours for correct display

        return {
            labels: xAxisLabels,
            datasets: [
                createDataset('Temperature', 'rgba(255, 165, 0, 0.75)', deviceData.map(item => item.Temperature)),
                createDataset('Light', 'rgba(0, 200, 0, 0.75)', deviceData.map(item => item.Light)),
                createDataset('Moisture', 'rgba(0, 0, 200, 0.75)', deviceData.map(item => item.Moisture)),
                createDataset('Conductivity', 'rgba(200, 0, 0, 0.75)', deviceData.map(item => item.Conductivity)),
            ],
            yAxisLabels: yAxisLabels, // Store Y-axis labels
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