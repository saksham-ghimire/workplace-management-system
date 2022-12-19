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
        document.getElementById('maxappuse'),
        config
    );


};


async function plot_user_activity_chart(from = Math.floor(Date.now() / 1000) - 604800, to = Math.floor(Date.now() / 1000)) {
    console.log("defined")
    const labels = ['Red', 'Orange', 'Yellow', 'Green', 'Blue'];
    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Dataset 1',
                data: [10, 20, 30, 4, 2],

            }
        ]
    };
    const config2 = {
        type: 'polarArea',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Chart.js Polar Area Chart'
                }
            }
        },
    };
    new Chart(
        document.getElementById('myChart2'),
        config2
    );

}