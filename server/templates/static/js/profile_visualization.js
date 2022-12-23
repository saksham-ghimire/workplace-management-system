async function plot_system_health_chart(hostname, from = Math.floor(Date.now() / 1000) - 1800, to = Math.floor(Date.now() / 1000)) {
    let dataq = await fetch(`http://localhost:8000/systeminfo/health/${hostname}?from_time=${from}&to_time=${to}`)
        .then((response) => response.json())
        .then(data => {
            return data
        })
        .catch(error => {
            console.error(error);
        });

    response = dataq
    Timestamps = []
    Cpus = []
    Temperatures = []
    RamUsage = []
    response.forEach(element => {

        Timestamps.push(new Date(element.timestamp * 1000).toLocaleTimeString("default"))
        Cpus.push(element.CpuPercent)
        Temperatures.push(element.Temperature)
        RamUsage.push(element.InUseRam.split(' ')[0])



    });

    const data = {
        labels: Timestamps,
        datasets: [
            {
                label: 'Cpu Usage',
                data: Cpus

            },
            {
                label: 'Temperature Usage',
                data: Temperatures
            },
            {
                label: 'RAM Usage',
                data: RamUsage
            }
        ]
    };

    const config4 = {
        type: 'line',
        data: data,
        options: {
            scales: {
                x: {
                    display: false
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                },
                title: {
                    display: true,
                    text: 'System Health Chart'
                }
            }
        },
    };
    new Chart(
        document.getElementById('system_chart'),
        config4
    );

}

async function plot_monitoring_process_chart(hostname, from = Math.floor(Date.now() / 1000) - 1800, to = Math.floor(Date.now() / 1000)) {
    process = ($('#mprocesses').val())

    let dataq = await fetch(`http://localhost:8000/monitoringprocesses?hostname=${hostname}&process=${process}&from_time=${from}&to_time=${to}`)
        .then((response) => response.json())
        .then(data => {
            console.log("erre", data)
            return data
        })
        .catch(error => {
            console.error(error);
        });

    response = dataq
    Timestamps = []
    Cpus = []
    RamUsage = []
    response.forEach(element => {

        Timestamps.push(new Date(element.timestamp * 1000).toLocaleTimeString("default"))
        Cpus.push(element.CpuPercent)
        RamUsage.push(element.MemoryPercent)



    });

    const data = {
        labels: Timestamps,
        datasets: [
            {
                label: 'Cpu Usage',
                data: Cpus

            },
            {
                label: 'Memory Usage',
                data: RamUsage
            }
        ]
    };

    const config4 = {
        type: 'line',
        data: data,
        options: {
            scales: {
                x: {
                    display: false
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                },
                title: {
                    display: true,
                    text: 'Monitoring Process Chart'
                }
            }
        },
    };
    if (Chart.getChart("monitoring_process_chart")) {
        Chart.getChart("monitoring_process_chart").destroy();
    }
    new Chart(
        document.getElementById('monitoring_process_chart'),
        config4
    )

}


async function plot_network_chart(hostname, from = Math.floor(Date.now() / 1000) - 60, to = Math.floor(Date.now() / 1000)) {
    console.log("from gre", hostname, from, to)
    let data = await fetch(`http://localhost:8000/network?hostname=${hostname}&from_time=${from}&to_time=${to}`)
        .then((response) => response.json())
        .then(data => {
            return data[data.length - 1];
        })
        .catch(error => {
            console.error(error);
        });

    response = data
    let labels = ["InputBytes", "OutputBytes", "OutputPkts", "InputPkts"]
    let plotData = [Math.abs(response.InputBytes) / 1000, response.OutputBytes / 1000, response.OutputPkt, response.InputPkt]

    $("#inputbytesCount").text(`${Math.abs(response.InputBytes) / 1000} KB`)
    $("#outputbytesCount").text(`${Math.abs(response.OutputBytes) / 1000} KB`)
    $("#inputpacketsCount").text(`${response.InputPkt}`)
    $("#outputpacketsCount").text(`${response.OutputPkt}`)

    const config = {
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
                    text: 'Network Chart'
                }
            }
        },
    };
    new Chart(
        document.getElementById('network_chart'),
        config
    );
}