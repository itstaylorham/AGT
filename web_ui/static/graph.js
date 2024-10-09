document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('api/sensor_data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const rawData = await response.json();
        const deviceDataMap = transformData(rawData);
        populateDeviceDropdown(deviceDataMap);

        const ctx = document.getElementById('main-dash');
        let lineGraph;

        // Initial graph setup
        const initialMac = Object.keys(deviceDataMap)[0];
        if (initialMac) {
            lineGraph = createLineGraph(ctx, deviceDataMap[initialMac]);
        }

        // Dropdown change event
        document.getElementById('device-selector').addEventListener('change', function() {
            if (lineGraph) {
                lineGraph.destroy();
            }
            lineGraph = createLineGraph(ctx, deviceDataMap[this.value]);
        });
    } catch (error) {
        console.error('Error:', error);
    }
});

// Function to normalize a value within a specified range
function normalize(value, min, max) {
    return (value - min) / (max - min);
}

function transformData(rawData) {
    let deviceDataMap = {};

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
            Conductivity: entry.conductivity
        });
    });

    return deviceDataMap;
}

function populateDeviceDropdown(deviceDataMap) {
    const dropdown = document.getElementById('device-selector');
    dropdown.innerHTML = Object.keys(deviceDataMap)
        .map(mac => `<option value="${mac}">${mac}</option>`)
        .join('');

    // Automatically trigger an update to display the initial device's data
    dropdown.dispatchEvent(new Event('change'));
}

function createLineGraph(ctx, deviceData) {
    const chartData = getChartData(deviceData);

    return new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            scales: {
                x: {
                    reverse: true // Set to true if you want the data to be displayed from right to left
                }
            }
        }
    });
}


function getXAxisLabels(timestamps, interval) {
    const labels = [];
    let startDate = new Date(timestamps[0]);
    let endDate = new Date(timestamps[timestamps.length - 1]);

    while (startDate <= endDate) {
        labels.push(startDate.toISOString().slice(0, 10)); // Get only the date part
        if (interval === 'week') {
            startDate.setDate(startDate.getDate() + 7); // Move to the next week
        } else if (interval === 'biweek') {
            startDate.setDate(startDate.getDate() + 14); // Move to the next biweek
        } else if (interval === 'month') {
            startDate.setMonth(startDate.getMonth() + 1); // Move to the next month
        } else if (interval === 'quarter') {
            startDate.setMonth(startDate.getMonth() + 3); // Move to the next quarter
        }
    }

    return labels;
}


function getChartData(deviceData) {
    const timestamps = deviceData.map(item => item.Timestamp);
    const temperature = deviceData.map(item => item.Temperature);
    const light = deviceData.map(item => item.Light);
    const moisture = deviceData.map(item => item.Moisture);
    const conductivity = deviceData.map(item => item.Conductivity);

    const xAxisLabels = timestamps.map(ts => ts.toISOString().slice(0, 10));

    return {
        labels: xAxisLabels,
        datasets: [
            {
                label: 'Temperature',
                backgroundColor: 'rgba(255, 165, 0, 0.75)',
                borderColor: 'rgba(255, 165, 0, 0.75)',
                data: temperature
            },
            {
                label: 'Light',
                backgroundColor: 'rgba(0, 200, 0, 0.75)',
                borderColor: 'rgba(0, 200, 0, 0.75)',
                data: light
            },
            {
                label: 'Moisture',
                backgroundColor: 'rgba(0, 0, 200, 0.75)',
                borderColor: 'rgba(0, 0, 200, 0.75)',
                data: moisture
            },
            {
                label: 'Conductivity',
                backgroundColor: 'rgba(200, 0, 0, 0.75)',
                borderColor: 'rgba(200, 0, 0, 0.75)',
                data: conductivity
            }
        ]
    };
}
