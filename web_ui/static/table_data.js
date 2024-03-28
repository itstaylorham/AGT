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

async function fetchSensorData() {
    try {
        const response = await fetch('/api/sensor_data');
        const data = await response.json();
        const sortedData = sortData(data).slice(0, 144);

        const table = document.getElementById('data-table');
        table.getElementsByTagName('tbody')[0].innerHTML = '';

        sortedData.forEach(deviceData => {
            // Convert to the user's local time and format it
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



document.addEventListener('DOMContentLoaded', fetchSensorData);
setInterval(fetchSensorData, 5000);
