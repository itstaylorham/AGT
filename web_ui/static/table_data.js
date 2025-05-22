function sortData(data) {
    return data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

function addNewRow(item) {
    let table = document.getElementById('data-table');
    let row = table.insertRow();

    let timestampCell = row.insertCell();
    timestampCell.textContent = item.Timestamp;

    let macCell = row.insertCell();
    macCell.textContent = item.MAC;

    let temperatureCell = row.insertCell();
    temperatureCell.textContent = item.Temperature;

    let moistureCell = row.insertCell();
    moistureCell.textContent = item.Moisture;

    let lightCell = row.insertCell();
    lightCell.textContent = item.Light;

    let conductivityCell = row.insertCell();
    conductivityCell.textContent = item.Conductivity;
}

function setupWebSocket() {
    const socket = new WebSocket('ws://api/sensor_data'); // Replace with your WebSocket URL

    socket.onmessage = (event) => {
        const deviceData = JSON.parse(event.data);
        let formattedTimestamp = new Date(deviceData.timestamp).toLocaleString();

        let item = {
            Timestamp: formattedTimestamp,
            MAC: deviceData.mac_address,
            Temperature: deviceData.temperature,
            Moisture: deviceData.moisture,
            Light: deviceData.light,
            Conductivity: deviceData.conductivity
        };
        addNewRow(item);

        // Optional: Maintain table size (e.g., keep last 144 rows)
        const table = document.getElementById('data-table');
        const rows = table.getElementsByTagName('tr');
        if (rows.length > 144) {
            table.deleteRow(rows.length - 1); // Remove oldest row
        }
    };

    socket.onopen = () => {
        console.log('WebSocket connection established');
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    socket.onclose = () => {
        console.log('WebSocket connection closed, attempting to reconnect...');
        setTimeout(setupWebSocket, 2000); // Reconnect after 2 seconds
    };
}

// Initial setup
document.addEventListener('DOMContentLoaded', () => {
    setupWebSocket();
    // Optional: Initial fetch to populate table
    fetchSensorData();
});

async function fetchSensorData() {
    try {
        const response = await fetch('/api/sensor_data');
        const data = await response.json();
        const sortedData = sortData(data).slice(0, 144);

        sortedData.forEach(deviceData => {
            let formattedTimestamp = new Date(deviceData.timestamp).toLocaleString();
            let item = {
                Timestamp: formattedTimestamp,
                MAC: deviceData.mac_address,
                Temperature: deviceData.temperature,
                Moisture: deviceData.moisture,
                Light: deviceData.light,
                Conductivity: deviceData.conductivity
            };
            addNewRow(item);
        });
    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}