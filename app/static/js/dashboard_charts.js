document.addEventListener('DOMContentLoaded', () => {
    const activeTasks = JSON.parse(document.getElementById('active-tasks-data').textContent);
    const completedLastMonth = JSON.parse(document.getElementById('completed-last-month-data').textContent);
    const completedLastWeek = JSON.parse(document.getElementById('completed-last-week-data').textContent);
    const completedLastDay = JSON.parse(document.getElementById('completed-last-day-data').textContent);

    const calculateBarWidth = (dataLength) => {
        return Math.max(0.1, Math.min(0.8, 8 / dataLength));
    };

    const calculateYAxisMax = (data) => {
        const maxValue = Math.max(...data);
        return Math.ceil(maxValue + maxValue * 0.3); // Add 30% padding
    };

    // Tasks Last Week Bar Chart
    const tasksLastWeekCtx = document.getElementById('tasksLastWeekChart').getContext('2d');
    new Chart(tasksLastWeekCtx, {
        type: 'bar',
        data: {
            labels: completedLastWeek.map(item => new Date(item.task_date).toLocaleDateString('en-US', { weekday: 'short' })),
            datasets: [{
                label: 'Completed Tasks',
                data: completedLastWeek.map(item => item.task_count),
                backgroundColor: '#F97316',
                borderColor: '#FB923C',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: calculateYAxisMax(completedLastWeek.map(item => item.task_count)),
                    title: {
                        display: true,
                        text: 'Number of Tasks',
                        color: '#F8F9FA',
                        font: { size: 14 }
                    },
                    ticks: { stepSize: 1, color: '#F8F9FA' },
                    grid: { color: '#F8F9FA' }
                },
                x: {
                    barPercentage: calculateBarWidth(completedLastWeek.length),
                    categoryPercentage: calculateBarWidth(completedLastWeek.length),
                    title: {
                        display: true,
                        text: 'Day',
                        color: '#F8F9FA',
                        font: { size: 14 }
                    },
                    ticks: { color: '#F8F9FA' },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { labels: { color: '#F8F9FA' } },
                tooltip: {
                    backgroundColor: '#F8F9FA',
                    titleColor: '#000000',
                    bodyColor: '#000000',
                    borderColor: '#F97316',
                    borderWidth: 1
                }
            }
        }
    });

    // Task Status Bar Chart
    const taskStatusCtx = document.getElementById('taskStatusChart').getContext('2d');
    new Chart(taskStatusCtx, {
        type: 'bar',
        data: {
            labels: ['Active Tasks', 'Completed (30 Days)'],
            datasets: [{
                label: 'Task Counts',
                data: [activeTasks, completedLastMonth],
                backgroundColor: ['#F97316', '#10B981'],
                borderColor: ['#FB923C', '#34D399'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: calculateYAxisMax([activeTasks, completedLastMonth]),
                    title: {
                        display: true,
                        text: 'Number of Tasks',
                        color: '#F8F9FA',
                        font: { size: 14 }
                    },
                    ticks: { stepSize: 1, color: '#F8F9FA' },
                    grid: { color: '#F8F9FA' }
                },
                x: {
                    barPercentage: calculateBarWidth(2),
                    categoryPercentage: calculateBarWidth(2),
                    title: {
                        display: true,
                        text: 'Status',
                        color: '#F8F9FA',
                        font: { size: 14 }
                    },
                    ticks: { color: '#F8F9FA' },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { labels: { color: '#F8F9FA' } },
                tooltip: {
                    backgroundColor: '#F8F9FA',
                    titleColor: '#000000',
                    bodyColor: '#000000',
                    borderColor: '#F97316',
                    borderWidth: 1
                }
            }
        }
    });

});