document.addEventListener('DOMContentLoaded', function() {
    fetchData();
});

function fetchData() {
    fetch('/api/metric_data')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('health-score-api-data');
            if (data.length > 0) {
                container.innerHTML = ''; // Clear the loading message

                // Process and display the health score
                data.forEach(entry => {
                    const div = document.createElement('div');
                    const roundedHealthScore = entry.health_score.toFixed(2); // Round to two decimal places
                    div.textContent = `Score: ${roundedHealthScore}`;
                    container.appendChild(div);
                });
            } else {
                container.textContent = 'No data available';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('health-score-api-data').textContent = 'Failed to load data';
        });
}