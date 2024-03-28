document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('api/graph_data');
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

function transformData(rawData) {
    let deviceDataMap = {};

    rawData.forEach(entry => {
        entry.MAC.forEach((mac, index) => {
            if (!deviceDataMap[mac]) {
                deviceDataMap[mac] = [];
            }

            deviceDataMap[mac].push({
                Timestamp: entry.Timestamp[index],
                Temperature: entry.Temperature[index],
                Light: entry.Light[index],
                Moisture: entry.Moisture[index],
                Conductivity: entry.Conductivity[index]
            });
        });
    });

    return deviceDataMap;
}

function transformData(rawData) {
    let deviceDataMap = {};

    rawData.forEach(entry => {
        entry.MAC.forEach((mac, index) => {
            if (!deviceDataMap[mac]) {
                deviceDataMap[mac] = [];
            }

            deviceDataMap[mac].push({
                Timestamp: entry.Timestamp[index],
                Temperature: entry.Temperature[index],
                Light: entry.Light[index],
                Moisture: entry.Moisture[index],
                Conductivity: entry.Conductivity[index]
            });
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
    return new Chart(ctx, {
        type: 'line',
        data: getChartData(deviceData),
        options: {}
    });
}

function getChartData(deviceData) {
    const timestamps = deviceData.map(item => item.Timestamp);
    const temperature = deviceData.map(item => item.Temperature);
    const light = deviceData.map(item => item.Light);
    const moisture = deviceData.map(item => item.Moisture);
    const conductivity = deviceData.map(item => item.Conductivity);

    return {
        labels: timestamps,
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
