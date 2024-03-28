function formatTimestampToEastern(Timestamp) {
    const date = new Date(BigInt(Math.round(Timestamp[0])));
    const options = {
        timeZone: "America/New_York", // Eastern Time
        hour12: false, // Use 12-hour format with AM/PM
        hour: '2-digit', // Display hour with 2 digits
        minute: '2-digit', // Display minute with 2 digits
        second: '2-digit', // Display second with 2 digits
    };
    return date.toLocaleString(undefined, options);
}

function sortData(data) {
    return data.sort((a, b) => b.Timestamp[0] - a.Timestamp[0]);
}

function addNewRow(item, tbody) {
    const row = tbody.insertRow();

    const timestampCell = row.insertCell();
    timestampCell.textContent = formatTimestamp(item.Timestamp);

    const macCell = row.insertCell();
    macCell.textContent = item.MAC;

    const temperatureCell = row.insertCell();
    temperatureCell.textContent = item.Temperature;

    const moistureCell = row.insertCell();
    moistureCell.textContent = item.Moisture;

    const lightCell = row.insertCell();
    lightCell.textContent = item.Light;

    const conductivityCell = row.insertCell();
    conductivityCell.textContent = item.Conductivity;

    return row;
}
function populateInitialTable(data) {
    const table = document.getElementById('data-table');
    const tbody = table.getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';

    data.forEach(item => {
        addNewRow(item, tbody);
    });
}

function updateTableWithNewRow(data) {
    const table = document.getElementById('data-table');
    const tbody = table.getElementsByTagName('tbody')[0];
    const initialRowCount = tbody.rows.length;

    if (data.length !== initialRowCount) {
        tbody.innerHTML = '';

        data.forEach((item, index) => {
            const row = addNewRow(item, tbody);

            if (index === 0 && data.length > initialRowCount) {
                row.classList.add('new-row');
                setTimeout(() => {
                    row.classList.remove('new-row');
                }, 2000);
            }
        });
    }
}

async function fetchSensorData() {
    try {
        const response = await fetch('/api/sensor_data');
        const data = await response.json();
        const sortedData = sortData(data).slice(0, 144);

        const table = document.getElementById('data-table');
        const tbody = table.getElementsByTagName('tbody')[0];

        // If the table is empty, populate the initial table
        if (tbody.rows.length === 0) {
            populateInitialTable(sortedData);
        } else {
            updateTableWithNewRow(sortedData);
        }
    } catch (error) {
        console.error('Error fetching sensor data:', error);
    }
}

// Fetch data and populate table on page load
document.addEventListener('DOMContentLoaded', fetchSensorData);

// Periodically fetch data and update the table
setInterval(() => {
    fetchSensorData();
}, 5000);



