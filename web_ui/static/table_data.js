function sortData(data) {
    return data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

function addNewRow(item) {
    let table = document.getElementById('data-table');
    let tbody = table.querySelector('tbody');
    let row = tbody.insertRow();
    
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

// Calculate statistical summary
function calculateStats(data, field) {
    const values = data.map(item => parseFloat(item[field])).filter(val => !isNaN(val));
    if (values.length === 0) return { min: 0, max: 0, avg: 0, median: 0, std: 0 };
    
    const sorted = [...values].sort((a, b) => a - b);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const avg = values.reduce((sum, val) => sum + val, 0) / values.length;
    
    // Median calculation
    const mid = Math.floor(sorted.length / 2);
    const median = sorted.length % 2 === 0 
        ? (sorted[mid - 1] + sorted[mid]) / 2 
        : sorted[mid];
    
    // Standard deviation
    const variance = values.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / values.length;
    const std = Math.sqrt(variance);
    
    return {
        min: min.toFixed(1),
        max: max.toFixed(1),
        avg: avg.toFixed(1),
        median: median.toFixed(1),
        std: std.toFixed(2)
    };
}

// Create or update statistical summary table
function updateStatisticalSummary(data) {
    const container = document.getElementById('health-score-api-data');
    
    // Calculate stats for each sensor type
    const tempStats = calculateStats(data, 'temperature');
    const moistureStats = calculateStats(data, 'moisture');
    const lightStats = calculateStats(data, 'light');
    const conductivityStats = calculateStats(data, 'conductivity');
    
    // Get unique device count
    const uniqueDevices = [...new Set(data.map(item => item.mac_address))];
    const deviceCount = uniqueDevices.length;
    const dataPoints = data.length;
    const timeSpan = data.length > 0 ? 
        Math.round((new Date(data[0].timestamp) - new Date(data[data.length - 1].timestamp)) / (1000 * 60 * 60)) : 0;
    
    container.innerHTML = `
        <div class="stats-summary">
            <h3>Statistical Summary</h3>
            <div class="stats-overview">
                <div class="stat-item">
                    <span class="stat-label">Active Devices:</span>
                    <span class="stat-value">${deviceCount}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Data Points:</span>
                    <span class="stat-value">${dataPoints}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Time Span:</span>
                    <span class="stat-value">${timeSpan}h</span>
                </div>
            </div>
            
            <table class="stats-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Min</th>
                        <th>Max</th>
                        <th>Average</th>
                        <th>Median</th>
                        <th>Std Dev</th>
                        <th>Unit</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Temperature</strong></td>
                        <td>${tempStats.min}</td>
                        <td>${tempStats.max}</td>
                        <td>${tempStats.avg}</td>
                        <td>${tempStats.median}</td>
                        <td>${tempStats.std}</td>
                        <td>°C</td>
                    </tr>
                    <tr>
                        <td><strong>Moisture</strong></td>
                        <td>${moistureStats.min}</td>
                        <td>${moistureStats.max}</td>
                        <td>${moistureStats.avg}</td>
                        <td>${moistureStats.median}</td>
                        <td>${moistureStats.std}</td>
                        <td>%</td>
                    </tr>
                    <tr>
                        <td><strong>Light</strong></td>
                        <td>${lightStats.min}</td>
                        <td>${lightStats.max}</td>
                        <td>${lightStats.avg}</td>
                        <td>${lightStats.median}</td>
                        <td>${lightStats.std}</td>
                        <td>lux</td>
                    </tr>
                    <tr>
                        <td><strong>Conductivity</strong></td>
                        <td>${conductivityStats.min}</td>
                        <td>${conductivityStats.max}</td>
                        <td>${conductivityStats.avg}</td>
                        <td>${conductivityStats.median}</td>
                        <td>${conductivityStats.std}</td>
                        <td>µS/cm</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}

async function fetchSensorData() {
    try {
        const response = await fetch('http://192.168.1.146:5000/api/sensor_data');
        const data = await response.json();
        const sortedData = sortData(data).slice(0, 144);
        
        // Update statistical summary
        updateStatisticalSummary(data);
        
        const table = document.getElementById('data-table');
        const tbody = table.querySelector('tbody');
        
        // Clear only the tbody content, NOT the entire table
        tbody.innerHTML = ''; 
        
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
        document.getElementById('health-score-api-data').innerHTML = 
            '<div class="error-message">Error loading statistical data</div>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchSensorData();
    setInterval(fetchSensorData, 5000); // Fetch every 5 seconds
});