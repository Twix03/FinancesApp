document.addEventListener("DOMContentLoaded", () => {
    echarts.init(document.querySelector("#trafficChart")).setOption({
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: '5%',
            left: 'center'
        },
        series: [{
            type: "pie",
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '18',
                    fontWeight: 'bold'
                }
            },
            // labelLine: {
            //     show: false
            // },
            data: [
                labels: labels,
                datesets:[
                    
                ]
            ],
        }],
        options: {
            title: {
                display: true,
                text: "Expenses per category",
            }
        }
    });
});
