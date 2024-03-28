document.addEventListener('DOMContentLoaded', async function () {
    try {
        const response = await fetch('api/sensor_data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const rawData = await response.json();

        let oneDayAgo = Date.now() - 24 * 60 * 60 * 100000000; // current time in ms minus 24 hours in ms

        let data = rawData
            .filter(item => item.Timestamp[0] >= oneDayAgo) // filter out old data
            .map(item => ({
                Timestamp: new Date(item.Timestamp[0]).toLocaleString(),                Temperature: item.Temperature[0],
                Light: item.Light[0],
                Moisture: item.Moisture[0],
                Conductivity: item.Conductivity[0]
            }));

        const timestamps = data.map(item => item.Timestamp);
        const temperature = data.map(item => item.Temperature);
        const light = data.map(item => item.Light);
        const moisture = data.map(item => item.Moisture);
        const conductivity = data.map(item => item.Conductivity);

        // Compute min and max values for each data category
        const temperatureRange = [Math.min(...temperature), Math.max(...temperature)];
        const moistureRange = [Math.min(...moisture), Math.max(...moisture)];
        const lightRange = [Math.min(...light), Math.max(...light)];
        const conductivityRange = [Math.min(...conductivity), Math.max(...conductivity)];

        let chartData = {
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

        const ctx = document.getElementById('analysis-dash').getContext('2d');
        let lineGraph = createLineGraph(chartData, ctx);

        let selectedTimeRange = timeRangeSelect.value;
            let timeRangeInDays;

            // Assign the appropriate time range in days based on the selected option
            switch (selectedTimeRange) {
                case '90':
                    timeRangeInDays = 90;
                    break;
                case '180':
                    timeRangeInDays = 180;
                    break;
                case '365':
                    timeRangeInDays = 365;
                    break;
                default:
                    timeRangeInDays = 0; // All Time or any other case
                    break;
            }

            let decided_range = Date.now() - timeRangeInDays * 24 * 60 * 60 * 1000;

            let filteredData = rawData
                .filter(item => item.Timestamp[0] >= decided_range)
                .map(item => ({
                    Timestamp: new Date(item.Timestamp[0]).toLocaleString(),
                    Temperature: item.Temperature[0],
                    Light: item.Light[0],
                    Moisture: item.Moisture[0],
                    Conductivity: item.Conductivity[0]
                }));


        const normalizeCheckbox = document.getElementById('normalize-data');
        normalizeCheckbox.addEventListener('change', function () {
            // Compute normalized or original data on-the-fly based on checkbox state
            chartData.datasets[0].data = data.map(item => this.checked ? (item.Temperature - temperatureRange[0]) / (temperatureRange[1] - temperatureRange[0]) : item.Temperature);
            chartData.datasets[1].data = data.map(item => this.checked ? (item.Light - lightRange[0]) / (lightRange[1] - lightRange[0]) : item.Light);
            chartData.datasets[2].data = data.map(item => this.checked ? (item.Moisture - moistureRange[0]) / (moistureRange[1] - moistureRange[0]) : item.Moisture);
            chartData.datasets[3].data = data.map(item => this.checked ? (item.Conductivity - conductivityRange[0]) / (conductivityRange[1] - conductivityRange[0]) : item.Conductivity);

            // Refresh the chart.
            updateChartData(lineGraph, chartData);
        });

    } catch (error) {
        console.error('Error:', error);
    }
});

function createLineGraph(data, ctx) {
    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Function to update the chart data
function updateChartData(chart, data) {
    chart.data = data;
    chart.update();
}
