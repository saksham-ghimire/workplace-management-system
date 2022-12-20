// This function is responsible for generating top 10 maximum used applications
async function plot_max_used_application_chart(from = Math.floor(Date.now() / 1000) - 604800, to = Math.floor(Date.now() / 1000)) {
    let data = await fetch(`http://localhost:8000/processruntime?from_time=${from}&to_time=${to}`)
        .then((response) => response.json())
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error(error);
        });

    response = data
    format_response = []
    for (let i = 0; i < response.length; i++) {
        format_response.push({ x: response[i].key, y: response[i].doc_count })
    }

    const config = {
        type: 'bar',
        data: {
            datasets: [{
                label: 'runtime',
                backgroundColor: '#2598d2	',
                borderColor: '#2598d2',

                data: format_response
            }]
        }
    };
    new Chart(
        document.getElementById('appUsageChart'),
        config
    );


};

async function plot_network_activity(from = Math.floor(Date.now() / 1000) - 604800, to = Math.floor(Date.now() / 1000)) {
    let data = await fetch(`http://localhost:8000/networkusage?from_time=${from}&to_time=${to}`)
        .then((response) => response.json())
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error(error);
        });

    response = data
    let labels = []
    let plotData = []
    for (let i = 0; i < response.length; i++) {
        labels.push(response[i].key)
        plotData.push(response[i].doc_count)

    }

    console.log(labels, plotData)

    const config3 = {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Dataset 1',
                    data: plotData,

                }
            ]
        },
        options: {
            maintainAspectRatio: false,

            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Doughnut Chart'
                }
            }
        },
    };
    new Chart(
        document.getElementById('netwrokActivityChart'),
        config3
    );

}


async function plot_user_activity_chart(from = Math.floor(Date.now() / 1000) - 604800, to = Math.floor(Date.now() / 1000)) {
    let data = await fetch(`http://localhost:8000/useractivity?from_time=${from}&to_time=${to}`)
        .then((response) => response.json())
        .then(data => {
            return data;
        })
        .catch(error => {
            console.error(error);
        });

    response = data

    let labels = []
    let plotData = []
    for (let i = 0; i < response.length; i++) {
        labels.push(response[i].key)
        plotData.push(response[i].doc_count)

    }
    console.log(labels, plotData)

    // const labels = ['Red', 'Orange', 'Yellow', 'Green', 'Blue'];

    const config2 = {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'User Activity Logs',
                    data: plotData,

                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'User Activity Chart'
                }
            }
        },
    };
    new Chart(
        document.getElementById('userActivityChart'),
        config2
    );

}



async function plot_system_health_chart(from = Math.floor(Date.now() / 1000) - 604800, to = Math.floor(Date.now() / 1000)) {

    const data = {
        labels: ["temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1", "temperature", "cpu", "cpu2", "cpu1"],
        datasets: [
            {
                label: 'Dataset 1',
                data: [10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81, 10, 20, 30, 81]

            },
            {
                label: 'Dataset 2',
                data: [40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11, 40, 30, 12, 11]
            }
        ]
    };

    const config4 = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Line Chart'
                }
            }
        },
    };
    new Chart(
        document.getElementById('system_chart2'),
        config4
    );
    new Chart(
        document.getElementById('system_chart'),
        config4
    );



}