let chartInstance;

function populateChartData() {
    const totalVotes = 100;
    const yesVotes = [45, 30, 25, 60, 70, 50];
    const noVotes = [15, 40, 20, 30, 25, 10];

    const winningYesVotes = yesVotes.map((yes, i) => yes > noVotes[i] ? yes - noVotes[i] : 0);
    const winningNoVotes = noVotes.map((no, i) => no > yesVotes[i] ? no - yesVotes[i] : 0);
    const emptyVotes = yesVotes.map((yes, i) => totalVotes - yes - noVotes[i]);
    const zeroedVotes = yesVotes.map((yes, i) => Math.min(yes, noVotes[i]));

    let gameNames = ['Gra 1', 'Gra 2', 'Gra 3', 'Gra 4', 'Gra 5', 'Gra 6'];

    return {
        labels: gameNames,
        datasets: [
            {
                label: 'Przewaga głosów na tak',
                data: winningYesVotes,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 0,
                maxBarThickness: 24,
            },
            {
                label: 'Pozostałe głosy na tak',
                data: zeroedVotes,
                backgroundColor: 'rgba(75, 192, 192, 0.3)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 0,
                maxBarThickness: 24,
            },
            {
                label: 'Brak',
                data: emptyVotes,
                backgroundColor: 'rgba(255, 255, 192, 0.1)',
                borderColor: 'rgba(184, 184, 184, 1)',
                borderWidth: 0,
                maxBarThickness: 24,
            },
            {
                label: 'Pozostałe głosy na nie',
                data: zeroedVotes,
                backgroundColor: 'rgba(255, 99, 132, 0.3)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 0,
                maxBarThickness: 24,
            },
            {
                label: 'Przewaga głosów na nie',
                data: winningNoVotes,
                backgroundColor: 'rgba(192, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 0,
                maxBarThickness: 24,
            },
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
                    stacked: true,
                },
                y: {
                    stacked: true,
                }
            },
        },
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('voteChart').getContext('2d');
    const chartData = populateChartData();

    chartInstance = createChart(ctx, chartData);
});