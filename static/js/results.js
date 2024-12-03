let chartInstance;

function populateChartData() {
    const winningYesVotes = yesVotes.map((yes, i) => yes > noVotes[i] ? yes - noVotes[i] : 0);
    const winningNoVotes = noVotes.map((no, i) => no > yesVotes[i] ? no - yesVotes[i] : 0);
    const emptyVotes = yesVotes.map((yes, i) => totalVotes - yes - noVotes[i]);
    const zeroedVotes = yesVotes.map((yes, i) => Math.min(yes, noVotes[i]));
    const maxBarThickness = 24;
    return {
        labels: gameNames,
        datasets: [
            {
                label: 'Tak (przewaga)',
                data: winningYesVotes,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 0,
                maxBarThickness: maxBarThickness,
            },
            {
                label: 'Tak',
                data: zeroedVotes,
                backgroundColor: 'rgba(75, 192, 192, 0.3)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 0,
                maxBarThickness: maxBarThickness,
            },
            {
                label: 'Brak',
                data: emptyVotes,
                backgroundColor: 'rgba(255, 255, 192, 0.1)',
                borderColor: 'rgba(184, 184, 184, 1)',
                borderWidth: 0,
                maxBarThickness: maxBarThickness,
            },
            {
                label: 'Nie',
                data: zeroedVotes,
                backgroundColor: 'rgba(255, 99, 132, 0.3)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 0,
                maxBarThickness: maxBarThickness,
            },
            {
                label: 'Nie (przewaga)',
                data: winningNoVotes,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 0,
                maxBarThickness: maxBarThickness,
            },
        ]
    };
}

function createChart(ctx, chartData) {
    return new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            maintainAspectRatio: false,
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
