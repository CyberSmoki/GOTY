let chartInstance;

function populateChartData() {
    let yesVotes = [45, 30, 25, 60, 70, 50];
    let emptyVotes = [95-45-15, 95-40-30, 95-20-25, 95-30-60, 0, 95-50-10];
    let noVotes = [15, 40, 20, 30, 25, 10];
    let gameNames = ['Gra 1', 'Gra 2', 'Gra 3', 'Gra 4', 'Gra 5', 'Gra 6'];

    return {
        labels: gameNames,
        datasets: [
            {
                label: 'Tak',
                data: yesVotes,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'Brak',
                data: emptyVotes,
                backgroundColor: 'rgba(184, 184, 184, 0.7)',
                borderColor: 'rgba(184, 184, 184, 1)',
                borderWidth: 1
            },
            {
                label: 'Nie',
                data: noVotes,
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }
            
        ]
    };
}

function createChart(ctx, chartData) {
    return new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            indexAxis: 'y', 
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true,
                    stacked: true
                },
                y: {
                    stacked: true
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('voteChart').getContext('2d');
    const chartData = populateChartData();

    chartInstance = createChart(ctx, chartData);
});