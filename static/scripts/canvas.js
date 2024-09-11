document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('successModal');
    const closeBtn = document.querySelector('.close-button');
    
    // Solo asigna los eventos si el modal y el botón de cierre existen
    if (modal && closeBtn) {
        closeBtn.onclick = function() {
            modal.style.display = 'none';
        };

        window.onclick = function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };
    }
});

const notClassifiedVideos = parseInt(document.getElementById('notClassifiedVideos').value, 10);; // Número total de videos (puedes cargar este valor dinámicamente)
const classifiedVideos = parseInt(document.getElementById('classifiedVideos').value, 10); // Número de videos almacenados para la tarea actual

const humorCount = parseInt(document.getElementById('humorCount').value, 10);; // Número total de videos (puedes cargar este valor dinámicamente)
const notHumorCount = parseInt(document.getElementById('notHumorCount').value, 10); // Número de videos almacenados para la tarea actual

const ctx4 = document.getElementById('videoChart2').getContext('2d');

// Crear el gráfico circular (doughnut)
const videoChart2 = new Chart(ctx4, {
    type: 'doughnut', // Gráfico circular de tipo 'doughnut'
    data: {
        labels: ['Number of videos with humor', 'Number of videos without humor'],
        datasets: [{
            data: [humorCount, notHumorCount],
            backgroundColor: ['#FFD700', '#1E90FF'], // Amarillo (Alegría) para el primer valor, Azul (Tristeza) para el segundo valor
            hoverBackgroundColor: ['#FFC300', '#187bcd'],
            borderWidth: 1,
            borderColor: '#f1f1f1',
            borderWidth: 3,
            hoverBorderWidth: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        layout: {
            padding: {
                top: 10,
                bottom: 10,
                left: 10,
                right: 10
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                        weight: 'bold',
                    },
                    boxWidth: 15,
                    boxHeight: 15,
                    padding: 20,  // Más espacio entre leyenda y gráfico
                    usePointStyle: true,  // Usar punto en vez de cuadro en la leyenda
                    textAlign: 'left',  // Alineación de las leyendas
                }
            },
            tooltip: {
                backgroundColor: '#fff',
                titleColor: '#333',
                bodyColor: '#333',
                borderColor: '#ddd',
                borderWidth: 1,
                bodyFont: {
                    size: 14,
                },
                callbacks: {
                    label: function(tooltipItem) {
                        // Esto ajusta el contenido del tooltip mostrando la etiqueta y el valor
                        let label = tooltipItem.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.raw;  // Mostrar el valor real del gráfico
                        return label;
                    }
                }
            }
        },
        animation: {
            animateRotate: true,
            duration: 1500,
            easing: 'easeInOutQuart'
        }
    }
});

const ctx = document.getElementById('videoChart').getContext('2d');

// Crear el gráfico circular (doughnut)
const videoChart = new Chart(ctx, {
    type: 'doughnut', // Gráfico circular de tipo 'doughnut'
    data: {
        labels: ['Number of classified videos', 'Number of not classified videos'],
        datasets: [{
            data: [classifiedVideos, notClassifiedVideos],
            backgroundColor: ['#28a745', '#6c757d'], // Verde para videos almacenados, gris para videos restantes
            hoverBackgroundColor: ['#218838', '#5a6268'], // Colores de hover
            borderWidth: 1,
            borderColor: '#f1f1f1',
            borderWidth: 3,
            hoverBorderWidth: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        layout: {
            padding: {
                top: 10,
                bottom: 10,
                left: 10,
                right: 10
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                        weight: 'bold',
                    },
                    boxWidth: 15,
                    boxHeight: 15,
                    padding: 20,  // Más espacio entre leyenda y gráfico
                    usePointStyle: true,  // Usar punto en vez de cuadro en la leyenda
                    textAlign: 'left',  // Alineación de las leyendas
                }
            },
            tooltip: {
                backgroundColor: '#fff',
                titleColor: '#333',
                bodyColor: '#333',
                borderColor: '#ddd',
                borderWidth: 1,
                bodyFont: {
                    size: 14,
                },
                callbacks: {
                    label: function(tooltipItem) {
                        // Esto ajusta el contenido del tooltip mostrando la etiqueta y el valor
                        let label = tooltipItem.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.raw;  // Mostrar el valor real del gráfico
                        return label;
                    }
                }
            }
        },
        animation: {
            animateRotate: true,
            duration: 1500,
            easing: 'easeInOutQuart'
        }
    }
});

const insultCount = parseInt(document.getElementById('insultCount').value, 10);; // Número total de videos (puedes cargar este valor dinámicamente)
const notInsultCount = parseInt(document.getElementById('notInsultCount').value, 10); // Número de videos almacenados para la tarea actual

const ctxInsult = document.getElementById('insultChart').getContext('2d');

// Crear el gráfico circular (doughnut)
const insultChart = new Chart(ctxInsult, {
    type: 'doughnut',
    data: {
        labels: ['Videos that do not contain insults', 'Videos containing insults'],
        datasets: [{
            data: [notInsultCount, insultCount],
            backgroundColor: ['#8e44ad', '#e74c3c'], // Morado para sin lenguaje inapropiado, Rojo para con lenguaje inapropiado
            hoverBackgroundColor: ['#71368a', '#c0392b'], // Tonos más oscuros para hover
            borderColor: '#f1f1f1',
            borderWidth: 3,
            hoverBorderWidth: 4,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        layout: {
            padding: {
                top: 10,
                bottom: 10,
                left: 10,
                right: 10
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                        weight: 'bold',
                    },
                    boxWidth: 15,
                    boxHeight: 15,
                    padding: 20,  // Más espacio entre leyenda y gráfico
                    usePointStyle: true,  // Usar punto en vez de cuadro en la leyenda
                    textAlign: 'left',  // Alineación de las leyendas
                }
            },
            tooltip: {
                backgroundColor: '#fff',
                titleColor: '#333',
                bodyColor: '#333',
                borderColor: '#ddd',
                borderWidth: 1,
                bodyFont: {
                    size: 14,
                },
                callbacks: {
                    label: function(tooltipItem) {
                        // Esto ajusta el contenido del tooltip mostrando la etiqueta y el valor
                        let label = tooltipItem.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.raw;  // Mostrar el valor real del gráfico
                        return label;
                    }
                }
            }
        },
        animation: {
            animateRotate: true,
            duration: 1500,
            easing: 'easeInOutQuart'
        }
    }
});


const improperCount = parseInt(document.getElementById('improperCount').value, 10);; // Número total de videos (puedes cargar este valor dinámicamente)
const notImproperCount = parseInt(document.getElementById('notImproperCount').value, 10); // Número de videos almacenados para la tarea actual

const ctxImproper = document.getElementById('improperChart').getContext('2d');

// Crear el gráfico circular (doughnut)
const improperChart = new Chart(ctxImproper, {
    type: 'doughnut', // Gráfico circular de tipo 'doughnut'
    data: {
        labels: ['Videos without improper language', 'Videos with improper language'],
        datasets: [{
            data: [notImproperCount, improperCount],
            backgroundColor: ['#3498db', '#e74c3c'], // Azul para sin insultos, Rojo para con insultos
            hoverBackgroundColor: ['#2980b9', '#c0392b'], // Tonos más oscuros para hover
            borderColor: '#f1f1f1',
            borderWidth: 3,
            hoverBorderWidth: 4,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        layout: {
            padding: {
                top: 10,
                bottom: 10,
                left: 10,
                right: 10
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                        weight: 'bold',
                    },
                    boxWidth: 15,
                    boxHeight: 15,
                    padding: 20,  // Más espacio entre leyenda y gráfico
                    usePointStyle: true,  // Usar punto en vez de cuadro en la leyenda
                    textAlign: 'left',  // Alineación de las leyendas
                }
            },
            tooltip: {
                backgroundColor: '#fff',
                titleColor: '#333',
                bodyColor: '#333',
                borderColor: '#ddd',
                borderWidth: 1,
                bodyFont: {
                    size: 14,
                },
                callbacks: {
                    label: function(tooltipItem) {
                        // Esto ajusta el contenido del tooltip mostrando la etiqueta y el valor
                        let label = tooltipItem.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.raw;  // Mostrar el valor real del gráfico
                        return label;
                    }
                }
            }
        },
        animation: {
            animateRotate: true,
            duration: 1500,
            easing: 'easeInOutQuart'
        }
    }
});

const toxicity0Count = parseInt(document.getElementById('toxicity0Count').value, 10); 
const toxicity1Count = parseInt(document.getElementById('toxicity1Count').value, 10);
const toxicity2Count = parseInt(document.getElementById('toxicity2Count').value, 10); 
const toxicity3Count = parseInt(document.getElementById('toxicity3Count').value, 10); 

const ctxToxicity = document.getElementById('toxicityChart').getContext('2d');

// Crear el gráfico circular (doughnut)
const toxicityChart = new Chart(ctxToxicity, {
    type: 'doughnut', // Gráfico circular de tipo 'doughnut'
    data: {
        labels: ['Videos in toxicity level 0', 'Videos in toxicity level 1', 'Videos in toxicity level 2', 'Videos in toxicity level 3'],
        datasets: [{
            data: [toxicity0Count, toxicity1Count, toxicity2Count, toxicity3Count],
            backgroundColor: ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c'], // Verde para nivel 0, amarillo nivel 1, naranja nivel 2, rojo nivel 3
            hoverBackgroundColor: ['#27ae60', '#f39c12', '#d35400', '#c0392b'], // Tonos más oscuros para hover
            borderColor: '#f1f1f1',
            borderWidth: 3,
            hoverBorderWidth: 4,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        layout: {
            padding: {
                top: 10,
                bottom: 10,
                left: 10,
                right: 10
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                        weight: 'bold',
                    },
                    boxWidth: 15,
                    boxHeight: 15,
                    padding: 20,  // Más espacio entre leyenda y gráfico
                    usePointStyle: true,  // Usar punto en vez de cuadro en la leyenda
                    textAlign: 'left',  // Alineación de las leyendas
                }
            },
            tooltip: {
                backgroundColor: '#fff',
                titleColor: '#333',
                bodyColor: '#333',
                borderColor: '#ddd',
                borderWidth: 1,
                bodyFont: {
                    size: 14,
                },
                callbacks: {
                    label: function(tooltipItem) {
                        // Esto ajusta el contenido del tooltip mostrando la etiqueta y el valor
                        let label = tooltipItem.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.raw;  // Mostrar el valor real del gráfico
                        return label;
                    }
                }
            }
        },
        animation: {
            animateRotate: true,
            duration: 1500,
            easing: 'easeInOutQuart'
        }
    }
});

const ctx2 = document.getElementById('sentimentChart').getContext('2d');

const averagePositive = parseFloat(document.getElementById('averagePositive').value, 10);
const averageNegative = parseFloat(document.getElementById('averageNegative').value, 10);
const averageNeutral = parseFloat(document.getElementById('averageNeutral').value, 10);
const averageNone = parseFloat(document.getElementById('averageNone').value, 10);

const sentimentData = {
    labels: ['Sentiments'], // Etiqueta única para la categoría de sentimientos
    datasets: [
        {
            label: 'Negative',
            data: [averageNegative],
            backgroundColor: '#dc3545',
            borderColor: '#dc3545',
            borderWidth: 1
        },
        {
            label: 'Neutral',
            data: [averageNeutral],
            backgroundColor: '#6c757d',
            borderColor: '#6c757d',
            borderWidth: 1
        },
        {
            label: 'None',
            data: [averageNone],
            backgroundColor: '#ffc107',
            borderColor: '#ffc107',
            borderWidth: 1
        },
        {
            label: 'Positive',
            data: [averagePositive],
            backgroundColor: '#28a745',
            borderColor: '#28a745',
            borderWidth: 1
        }
    ]
};


const sentimentChart = new Chart(ctx2, {
    type: 'bar',
    data: sentimentData,
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Probability'
                }
            }
        }
    }
});



const ctx3 = document.getElementById('emotionChart').getContext('2d');

const averageAnger = parseFloat(document.getElementById('averageAnger').value, 10);
const averageDisgust = parseFloat(document.getElementById('averageDisgust').value, 10);
const averageFear = parseFloat(document.getElementById('averageFear').value, 10);
const averageJoy = parseFloat(document.getElementById('averageJoy').value, 10);
const averageSadness = parseFloat(document.getElementById('averageSadness').value, 10);
const averageSurprise = parseFloat(document.getElementById('averageSurprise').value, 10);

const emotionData = {
    labels: ['Emotions'], // Etiqueta única para la categoría de sentimientos
    datasets: [
        {
            label: 'Anger',
            data: [averageAnger],
            backgroundColor: '#dc3545',
            borderColor: '#dc3545',
            borderWidth: 1
        },
        {
            label: 'Disgust',
            data: [averageDisgust],
            backgroundColor: '#6c757d',
            borderColor: '#6c757d',
            borderWidth: 1
        },
        {
            label: 'Fear',
            data: [averageFear],
            backgroundColor: '#ffc107',
            borderColor: '#ffc107',
            borderWidth: 1
        },
        {
            label: 'Joy',
            data: [averageJoy],
            backgroundColor: '#28a745',
            borderColor: '#28a745',
            borderWidth: 1
        },
        {
            label: 'Sadness',
            data: [averageSadness],
            backgroundColor: '#33ff57',
            borderColor: '#33ff57',
            borderWidth: 1
        },
        {
            label: 'Surprise',
            data: [averageSurprise],
            backgroundColor: '#1abc9c',
            borderColor: '#1abc9c',
            borderWidth: 1
        }
    ]
};


const emotionChart = new Chart(ctx3, {
    type: 'bar',
    data: emotionData,
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Probability'
                }
            }
        }
    }
});

    const listDaysString = document.getElementById('listDays').value;
    const listDays = JSON.parse(listDaysString);
    
    const listWeeksString = document.getElementById('listWeeks').value;
    const listWeeks = JSON.parse(listWeeksString);

    const listMonthsString = document.getElementById('listMonths').value;
    const listMonths = JSON.parse(listMonthsString);

    // Extraer las etiquetas y datos de cada división
    const daysLabels = [];
    const daysVideosCounts = [];

    const averageAggressiveDays = [];
    const averageNotAggressiveDays = [];

    const averageArgumentativeDays = [];
    const averageNotArgumentativeDays = [];

    const averageOffensiveDays = [];
    const averageNotOffensiveDays = [];

    const averageConstructiveDays = [];
    const averageNotConstructiveDays = [];

    const averageIntolerantDays = [];
    const averageTolerantDays = [];

    const averageStereotypeDays = [];
    const averageNotStereotypeDays = []

    // Recorre la lista de días
    listDays.forEach(dayEntry => {
        // Almacena el label (día)
        daysLabels.push(dayEntry.day);

        // Almacena la cantidad de videos en list_videos
        daysVideosCounts.push(dayEntry.list_videos.length);

        let aux = dayEntry.aggressiveness;
        aux.forEach(aggressive => { 
            averageAggressiveDays.push(aggressive.averageAggressive);
            averageNotAggressiveDays.push(aggressive.averageNotAggressive);
        });

        aux = dayEntry.argumentative;
        aux.forEach(argumentative => {
            averageArgumentativeDays.push(argumentative.averageArgumentative);
            averageNotArgumentativeDays.push(argumentative.averageNotArgumentative);
        });

        aux = dayEntry.offensiveness;
        aux.forEach(offensive => {
            averageOffensiveDays.push(offensive.averageOffensive);
            averageNotOffensiveDays.push(offensive.averageNotOffensive);
        });

        aux = dayEntry.constructiveness;
        aux.forEach(constructive => {
            averageConstructiveDays.push(constructive.averageConstructive);
            averageNotConstructiveDays.push(constructive.averageNotConstructive);
        });

        aux = dayEntry.intolerance;
        aux.forEach(intolerance => {
            averageIntolerantDays.push(intolerance.averageIntolerant);
            averageTolerantDays.push(intolerance.averageTolerant);
        });

        aux = dayEntry.stereotype;
        aux.forEach(stereotype => {
            averageStereotypeDays.push(stereotype.averageStereotypes);
            averageNotStereotypeDays.push(stereotype.averageNotStereotypes);
        });
    });

    const weeksLabels = [];
    const weeksVideosCounts = [];

    const averageAggressiveWeeks = [];
    const averageNotAggressiveWeeks = [];

    const averageArgumentativeWeeks = [];
    const averageNotArgumentativeWeeks = [];

    const averageOffensiveWeeks = [];
    const averageNotOffensiveWeeks = [];

    const averageConstructiveWeeks = [];
    const averageNotConstructiveWeeks = [];

    const averageIntolerantWeeks = [];
    const averageTolerantWeeks = [];

    const averageStereotypeWeeks = [];
    const averageNotStereotypeWeeks = [];

    // Recorre la lista de semanas
    listWeeks.forEach(weekEntry => {
        // Almacena el label (semanas)
        weeksLabels.push(weekEntry.week_start);

        // Almacena la cantidad de videos en list_videos
        weeksVideosCounts.push(weekEntry.list_videos.length);

        let aux = weekEntry.aggressiveness;
        aux.forEach(aggressive => { 
            averageAggressiveWeeks.push(aggressive.averageAggressive);
            averageNotAggressiveWeeks.push(aggressive.averageNotAggressive);
        });

        aux = weekEntry.argumentative;
        aux.forEach(argumentative => {
            averageArgumentativeWeeks.push(argumentative.averageArgumentative);
            averageNotArgumentativeWeeks.push(argumentative.averageNotArgumentative);
        });

        aux = weekEntry.offensiveness;
        aux.forEach(offensive => {
            averageOffensiveWeeks.push(offensive.averageOffensive);
            averageNotOffensiveWeeks.push(offensive.averageNotOffensive);
        });

        aux = weekEntry.constructiveness;
        aux.forEach(constructive => {
            averageConstructiveWeeks.push(constructive.averageConstructive);
            averageNotConstructiveWeeks.push(constructive.averageNotConstructive);
        });

        aux = weekEntry.intolerance;
        aux.forEach(intolerance => {
            averageIntolerantWeeks.push(intolerance.averageIntolerant);
            averageTolerantWeeks.push(intolerance.averageTolerant);
        });

        aux = weekEntry.stereotype;
        aux.forEach(stereotype => {
            averageStereotypeWeeks.push(stereotype.averageStereotypes);
            averageNotStereotypeWeeks.push(stereotype.averageNotStereotypes);
        });
    });

    const monthsLabels = [];
    const monthsVideosCounts = [];

    const averageAggressiveMonths= [];
    const averageNotAggressiveMonths = [];

    const averageArgumentativeMonths = [];
    const averageNotArgumentativeMonths = [];

    const averageOffensiveMonths = [];
    const averageNotOffensiveMonths = [];

    const averageConstructiveMonths = [];
    const averageNotConstructiveMonths = [];

    const averageIntolerantMonths = [];
    const averageTolerantMonths = [];

    const averageStereotypeMonths = [];
    const averageNotStereotypeMonths = [];

    // Recorre la lista de meses
    listMonths.forEach(monthEntry => {
        // Almacena el label (meses)
        monthsLabels.push(monthEntry.month);

        // Almacena la cantidad de videos en list_videos
        monthsVideosCounts.push(monthEntry.list_videos.length);

        let aux = monthEntry.aggressiveness;
        aux.forEach(aggressive => { 
            averageAggressiveMonths.push(aggressive.averageAggressive);
            averageNotAggressiveMonths.push(aggressive.averageNotAggressive);
        });

        aux = monthEntry.argumentative;
        aux.forEach(argumentative => {
            averageArgumentativeMonths.push(argumentative.averageArgumentative);
            averageNotArgumentativeMonths.push(argumentative.averageNotArgumentative);
        });

        aux = monthEntry.offensiveness;
        aux.forEach(offensive => {
            averageOffensiveMonths.push(offensive.averageOffensive);
            averageNotOffensiveMonths.push(offensive.averageNotOffensive);
        });

        aux = monthEntry.constructiveness;
        aux.forEach(constructive => {
            averageConstructiveMonths.push(constructive.averageConstructive);
            averageNotConstructiveMonths.push(constructive.averageNotConstructive);
        });

        aux = monthEntry.intolerance;
        aux.forEach(intolerance => {
            averageIntolerantWeeks.push(intolerance.averageIntolerant);
            averageTolerantWeeks.push(intolerance.averageTolerant);
        });

        aux = monthEntry.stereotype;
        aux.forEach(stereotype => {
            averageStereotypeMonths.push(stereotype.averageStereotypes);
            averageNotStereotypeMonths.push(stereotype.averageNotStereotypes);
        });
    });

    // Crear el gráfico inicial con los datos de días
    const ctx10 = document.getElementById('timelineChart').getContext('2d');
    let timelineChart = new Chart(ctx10, {
        type: 'line',
        data: {
            labels: daysLabels,  // Usamos los días como etiquetas
            datasets: [{
                label: 'Videos per day',
                data: daysVideosCounts,  // Número de videos por día
                borderColor: 'rgba(255, 99, 132, 1)', // Color de la línea
                backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo de los puntos
                borderWidth: 1, // Grosor de la línea
                pointStyle: 'circle', // Estilo de los puntos
                pointRadius: 5, // Tamaño de los puntos
                fill: false // No rellenar debajo de la línea
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Time line per days'
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Dates'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Count of videos'
                    },
                    beginAtZero: true
                }
            }
        }
    });

    // Función para actualizar la gráfica según la opción seleccionada
    document.getElementById('timeSelector').addEventListener('change', function() {
        const selectedOption = this.value;

        if (selectedOption === 'days') {
            timelineChart.data.labels = daysLabels;
            timelineChart.data.datasets[0].data = daysVideosCounts;
            timelineChart.data.datasets[0].label = 'Videos per days';
            timelineChart.data.datasets[0].borderColor = 'rgba(255, 99, 132, 1)';
            timelineChart.data.datasets[0].backgroundColor = 'rgba(255, 99, 132, 0.2)';
            timelineChart.data.datasets[0].borderWidth = 1;
            timelineChart.data.datasets[0].pointStyle = 'circle';
        } else if (selectedOption === 'weeks') {
            timelineChart.data.labels = weeksLabels;
            timelineChart.data.datasets[0].data = weeksVideosCounts;
            timelineChart.data.datasets[0].label = 'Videos per weeks';
            timelineChart.data.datasets[0].borderColor = 'rgba(54, 162, 235, 1)';
            timelineChart.data.datasets[0].backgroundColor = 'rgba(54, 162, 235, 0.2)';
            timelineChart.data.datasets[0].borderWidth = 1;
            timelineChart.data.datasets[0].pointStyle = 'rect';
        } else if (selectedOption === 'months') {
            timelineChart.data.labels = monthsLabels;
            timelineChart.data.datasets[0].data = monthsVideosCounts;
            timelineChart.data.datasets[0].label = 'Videos per months';
            timelineChart.data.datasets[0].borderColor = 'rgba(153, 102, 255, 1)';
            timelineChart.data.datasets[0].backgroundColor = 'rgba(153, 102, 255, 0.2)';
            timelineChart.data.datasets[0].borderWidth = 1;
            timelineChart.data.datasets[0].pointStyle = 'triangle';
        }

        timelineChart.update();  // Actualizar la gráfica con los nuevos datos
    });

const ctx6 = document.getElementById('ironyChart').getContext('2d');

const averageIronic = parseFloat(document.getElementById('averageIronic').value, 10);
const averageNotIronic = parseFloat(document.getElementById('averageNotIronic').value, 10);

// Datos del gráfico (ejemplo de porcentajes)
const dataIronic = {
    labels: ['Ironic', 'Not Ironic'],
    values: [averageIronic, averageNotIronic],  // Sumarán el 100%
    colors: ['#FF6384', '#36A2EB']
};

// Función para dibujar el gráfico de quesitos
function drawPieChart(ctx6, dataIronic) {
    let totalValue = data.values.reduce((acc, val) => acc + val, 0);
    let startAngle = 0;

    dataIronic.values.forEach((value, index) => {
        let formattedValue = parseFloat(value.toFixed(2));
        let sliceAngle = (formattedValue / totalValue) * 2 * Math.PI;
        ctx6.beginPath();
        ctx6.moveTo(200, 200);  // Punto central del gráfico (x, y)
        ctx6.arc(200, 200, 150, startAngle, startAngle + sliceAngle);  // Dibujar el sector
        ctx6.closePath();

        // Rellenar el sector con su color correspondiente
        ctx6.fillStyle = dataIronic.colors[index];
        ctx6.fill();

        // Calcular la posición para el label (en el centro de cada porción)
        let middleAngle = startAngle + sliceAngle / 2;
        let labelX = 200 + (Math.cos(middleAngle) * 100);  // Coordenada X del label
        let labelY = 200 + (Math.sin(middleAngle) * 100);  // Coordenada Y del label

        // Dibujar el texto (label) en el gráfico
        ctx6.fillStyle = "#000";  // Color del texto
        ctx6.font = "16px Arial";  // Estilo de la fuente
        ctx6.textAlign = "center";  // Alinear el texto
        ctx6.fillText(`${formattedValue}%`, labelX, labelY);  // Dibujar el label

        // Actualizar el ángulo de inicio para el siguiente sector
        startAngle += sliceAngle;
    });
}

// Llamada a la función para dibujar el gráfico
drawPieChart(ctx6, dataIronic);

const ctx7 = document.getElementById('sarcasmChart').getContext('2d');

const averageSarcastic = parseFloat(document.getElementById('averageSarcastic').value, 10);
const averageNotSarcastic = parseFloat(document.getElementById('averageNotSarcastic').value, 10);

// Datos del gráfico (ejemplo de porcentajes)
const dataSarcastic= {
    labels: ['Sarcastic', 'Not Sarcastic'],
    values: [averageSarcastic, averageNotSarcastic],  // Sumarán el 100%
    colors: ['#FFCE56', '#4BC0C0']
};

// Función para dibujar el gráfico de quesitos
function drawPieChart(ctx7, dataSarcastic) {
    let totalValue = data.values.reduce((acc, val) => acc + val, 0);
    let startAngle = 0;

    dataSarcastic.values.forEach((value, index) => {
        let formattedValue = parseFloat(value.toFixed(2));
        let sliceAngle = (formattedValue / totalValue) * 2 * Math.PI;
        ctx7.beginPath();
        ctx7.moveTo(200, 200);  // Punto central del gráfico (x, y)
        ctx7.arc(200, 200, 150, startAngle, startAngle + sliceAngle);  // Dibujar el sector
        ctx7.closePath();

        // Rellenar el sector con su color correspondiente
        ctx7.fillStyle = dataSarcastic.colors[index];
        ctx7.fill();

        // Calcular la posición para el label (en el centro de cada porción)
        let middleAngle = startAngle + sliceAngle / 2;
        let labelX = 200 + (Math.cos(middleAngle) * 100);  // Coordenada X del label
        let labelY = 200 + (Math.sin(middleAngle) * 100);  // Coordenada Y del label

        // Dibujar el texto (label) en el gráfico
        ctx7.fillStyle = "#000";  // Color del texto
        ctx7.font = "16px Arial";  // Estilo de la fuente
        ctx7.textAlign = "center";  // Alinear el texto
        ctx7.fillText(`${formattedValue}%`, labelX, labelY);  // Dibujar el label

        // Actualizar el ángulo de inicio para el siguiente sector
        startAngle += sliceAngle;
    });
}

// Llamada a la función para dibujar el gráfico
drawPieChart(ctx7, dataSarcastic);

const ctx8 = document.getElementById('hateChart').getContext('2d');

const averageHate = parseFloat(document.getElementById('averageHate').value, 10);
const averageNotHate = parseFloat(document.getElementById('averageNotHate').value, 10);

// Datos del gráfico (ejemplo de porcentajes)
const dataHate= {
    labels: ['Hate', 'Not Hate'],
    values: [averageHate, averageNotHate],  // Sumarán el 100%
    colors: ['#1abc9c', '#b1ec0f']
};

// Función para dibujar el gráfico de quesitos
function drawPieChart(ctx8, dataHate) {
    let totalValue = dataHate.values.reduce((acc, val) => acc + val, 0);
    let startAngle = 0;

    dataHate.values.forEach((value, index) => {
        let formattedValue = parseFloat(value.toFixed(2));
        let sliceAngle = (formattedValue / totalValue) * 2 * Math.PI;
        ctx8.beginPath();
        ctx8.moveTo(200, 200);  // Punto central del gráfico (x, y)
        ctx8.arc(200, 200, 150, startAngle, startAngle + sliceAngle);  // Dibujar el sector
        ctx8.closePath();

        // Rellenar el sector con su color correspondiente
        ctx8.fillStyle = dataHate.colors[index];
        ctx8.fill();

        // Calcular la posición para el label (en el centro de cada porción)
        let middleAngle = startAngle + sliceAngle / 2;
        let labelX = 200 + (Math.cos(middleAngle) * 100);  // Coordenada X del label
        let labelY = 200 + (Math.sin(middleAngle) * 100);  // Coordenada Y del label

        // Dibujar el texto (label) en el gráfico
        ctx8.fillStyle = "#000";  // Color del texto
        ctx8.font = "16px Arial";  // Estilo de la fuente
        ctx8.textAlign = "center";  // Alinear el texto
        ctx8.fillText(`${formattedValue}%`, labelX, labelY);  // Dibujar el label

        // Actualizar el ángulo de inicio para el siguiente sector
        startAngle += sliceAngle;
    });
}

// Llamada a la función para dibujar el gráfico
drawPieChart(ctx8, dataHate);

const ctx11 = document.getElementById('mockeryChart').getContext('2d');

const averageMockery = parseFloat(document.getElementById('averageMockery').value, 10);
const averageNotMockery = parseFloat(document.getElementById('averageNotMockery').value, 10);

// Datos del gráfico (ejemplo de porcentajes)
const dataMockery= {
    labels: ['Mockery', 'Not Mockery'],
    values: [averageMockery, averageNotMockery],  // Sumarán el 100%
    colors: ['#ecb008', '#44be0c']
};

// Función para dibujar el gráfico de quesitos
function drawPieChart(ctx11, dataMockery) {
    let totalValue = dataMockery.values.reduce((acc, val) => acc + val, 0);
    let startAngle = 0;

    dataMockery.values.forEach((value, index) => {
        let formattedValue = parseFloat(value.toFixed(2));
        let sliceAngle = (formattedValue / totalValue) * 2 * Math.PI;
        ctx11.beginPath();
        ctx11.moveTo(200, 200);  // Punto central del gráfico (x, y)
        ctx11.arc(200, 200, 150, startAngle, startAngle + sliceAngle);  // Dibujar el sector
        ctx11.closePath();

        // Rellenar el sector con su color correspondiente
        ctx11.fillStyle = dataMockery.colors[index];
        ctx11.fill();

        // Calcular la posición para el label (en el centro de cada porción)
        let middleAngle = startAngle + sliceAngle / 2;
        let labelX = 200 + (Math.cos(middleAngle) * 100);  // Coordenada X del label
        let labelY = 200 + (Math.sin(middleAngle) * 100);  // Coordenada Y del label

        // Dibujar el texto (label) en el gráfico
        ctx11.fillStyle = "#000";  // Color del texto
        ctx11.font = "16px Arial";  // Estilo de la fuente
        ctx11.textAlign = "center";  // Alinear el texto
        ctx11.fillText(`${formattedValue}%`, labelX, labelY);  // Dibujar el label

        // Actualizar el ángulo de inicio para el siguiente sector
        startAngle += sliceAngle;
    });
}

// Llamada a la función para dibujar el gráfico
drawPieChart(ctx11, dataMockery);

const ctx9 = document.getElementById('myLineChart').getContext('2d');

    const myLineChart = new Chart(ctx9, {
        type: 'line', // Tipo de gráfico
        data: {
            labels: daysLabels, // Las etiquetas del eje X
            datasets: [
                {
                    label: 'Agressive',
                    data: averageAggressiveDays, // Datos de la primera línea
                    borderColor: 'rgba(255, 99, 132, 1)', // Color de la línea
                    backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo de los puntos
                    borderWidth: 1, // Grosor de la línea
                    pointStyle: 'circle', // Estilo de los puntos
                    pointRadius: 5, // Tamaño de los puntos
                    fill: false // No rellenar debajo de la línea
                },
                {
                    label: 'Not Agressive',
                    data: averageNotAggressiveDays, // Datos de la segunda línea
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderWidth: 1,
                    pointStyle: 'rect', // Estilo de los puntos (cuadrados)
                    pointRadius: 5,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top', // Posición de la leyenda
                },
            },
            scales: {
                x: {
                    beginAtZero: true, // Comienza desde 0 en el eje X
                },
                y: {
                    beginAtZero: true // Comienza desde 0 en el eje Y
                }
            }
        }
    });

// Función para actualizar la gráfica según la opción seleccionada
document.getElementById('classSelector').addEventListener('change', function() {
    const selectedOption = this.value;

    if (selectedOption === 'aggressive') {
        myLineChart.data.datasets[0].data = averageAggressiveDays;
        myLineChart.data.datasets[1].data = averageNotAggressiveDays;
        myLineChart.data.datasets[0].label = 'Aggressive';
        myLineChart.data.datasets[1].label = 'Not Aggresive';
    } else if (selectedOption === 'argumentative') {
        myLineChart.data.datasets[0].data = averageArgumentativeDays;
        myLineChart.data.datasets[1].data = averageNotArgumentativeDays;
        myLineChart.data.datasets[0].label = 'Argumentative';
        myLineChart.data.datasets[1].label = 'Not Argumentative';
    } else if (selectedOption === 'offensive') {
        myLineChart.data.datasets[0].data = averageOffensiveDays;
        myLineChart.data.datasets[1].data = averageNotOffensiveDays;
        myLineChart.data.datasets[0].label = 'Offensive';
        myLineChart.data.datasets[1].label = 'Not Offensive';
    } else if (selectedOption === 'constructive') {
        myLineChart.data.datasets[0].data = averageConstructiveDays;
        myLineChart.data.datasets[1].data = averageNotConstructiveDays;
        myLineChart.data.datasets[0].label = 'Constructive';
        myLineChart.data.datasets[1].label = 'Not Constructive';
    } else if (selectedOption === 'intolerance') {
        myLineChart.data.datasets[0].data = averageTolerantDays;
        myLineChart.data.datasets[1].data = averageIntolerantDays;
        myLineChart.data.datasets[0].label = 'Tolerant';
        myLineChart.data.datasets[1].label = 'Intolerant';
    } else if (selectedOption === 'stereotype') {
        myLineChart.data.datasets[0].data = averageStereotypeDays;
        myLineChart.data.datasets[1].data = averageNotStereotypeDays;
        myLineChart.data.datasets[0].label = 'Stereotypes';
        myLineChart.data.datasets[1].label = 'Not Stereotypes';
    }

    myLineChart.update();  // Actualizar la gráfica con los nuevos datos
});

// Función para actualizar la gráfica según la opción seleccionada
document.getElementById('timeSelector2').addEventListener('change', function() {
    const selectedOption = this.value;

    if (selectedOption === 'days') {
        myLineChart.data.labels = daysLabels;
        if(myLineChart.data.datasets[0] == 'Aggressive') {
            myLineChart.data.datasets[0].data = averageAggressiveDays;
            myLineChart.data.datasets[1].data = averageNotAggressiveDays;
        } else if (myLineChart.data.datasets[0] == 'Argumentative') {
            myLineChart.data.datasets[0].data = averageArgumentativeDays;
            myLineChart.data.datasets[1].data = averageNotArgumentativeDays;
        } else if (myLineChart.data.datasets[0] == 'Offensive') {
            myLineChart.data.datasets[0].data = averageOffensiveDays;
            myLineChart.data.datasets[1].data = averageNotOffensiveDays;
        } else if (myLineChart.data.datasets[0] == 'Constructive') {
            myLineChart.data.datasets[0].data = averageConstructiveDays;
            myLineChart.data.datasets[1].data = averageNotConstructiveDays;
        } else if (myLineChart.data.datasets[0] == 'Stereotype') {
            myLineChart.data.datasets[0].data = averageStereotypeDays;
            myLineChart.data.datasets[1].data = averageNotStereotypeDays;
        } else {
            myLineChart.data.datasets[0].data = averageTolerantDays;
            myLineChart.data.datasets[1].data = averageIntolerantDays;
        }
        
    } else if (selectedOption === 'weeks') {
        myLineChart.data.labels = weeksLabels;
        if(myLineChart.data.datasets[0] == 'Aggressive') {
            myLineChart.data.datasets[0].data = averageAggressiveWeeks;
            myLineChart.data.datasets[1].data = averageNotAggressiveWeeks;
        } else if (myLineChart.data.datasets[0] == 'Argumentative') {
            myLineChart.data.datasets[0].data = averageArgumentativeWeeks;
            myLineChart.data.datasets[1].data = averageNotArgumentativeWeeks;
        } else if (myLineChart.data.datasets[0] == 'Offensive') {
            myLineChart.data.datasets[0].data = averageOffensiveWeeks;
            myLineChart.data.datasets[1].data = averageNotOffensiveWeeks;
        } else if (myLineChart.data.datasets[0] == 'Constructive'){
            myLineChart.data.datasets[0].data = averageConstructiveWeeks;
            myLineChart.data.datasets[1].data = averageNotConstructiveWeeks;
        } else if (myLineChart.data.datasets[0] == 'Stereotypes') {
            myLineChart.data.datasets[0].data = averageStereotypeWeeks;
            myLineChart.data.datasets[1].data = averageNotStereotypeWeeks;
        } else {
            myLineChart.data.datasets[0].data = averageTolerantWeeks;
            myLineChart.data.datasets[1].data = averageIntolerantWeeks;
        }
    } else if (selectedOption === 'months') {
        myLineChart.data.labels = monthsLabels;
        if(myLineChart.data.datasets[0] == 'Aggressive') {
            myLineChart.data.datasets[0].data = averageAggressiveMonths;
            myLineChart.data.datasets[1].data = averageNotAggressiveMonths;
        } else if (myLineChart.data.datasets[0] == 'Argumentative') {
            myLineChart.data.datasets[0].data = averageArgumentativeMonths;
            myLineChart.data.datasets[1].data = averageNotArgumentativeMonths;
        } else if (myLineChart.data.datasets[0] == 'Offensive') {
            myLineChart.data.datasets[0].data = averageOffensiveMonths;
            myLineChart.data.datasets[1].data = averageNotOffensiveMonths;
        } else if (myLineChart.data.datasets[0] == 'Constructive') {
            myLineChart.data.datasets[0].data = averageConstructiveMonths;
            myLineChart.data.datasets[1].data = averageNotConstructiveMonths;
        } else if (myLineChart.data.datasets[0] == 'Stereotypes') {
            myLineChart.data.datasets[0].data = averageStereotypeMonths;
            myLineChart.data.datasets[1].data = averageNotStereotypeMonths;
        } else {
            myLineChart.data.datasets[0].data = averageTolerantMonths;
            myLineChart.data.datasets[1].data = averageIntolerantMonths;
        }
    }

    myLineChart.update();  // Actualizar la gráfica con los nuevos datos
});

//const ctx5 = document.getElementById('profileChart').getContext('2d');

const averageAgreeable = parseFloat(document.getElementById('averageAgreeable').value, 10);
const averageConscientious = parseFloat(document.getElementById('averageConscientious').value, 10);
const averageOpen = parseFloat(document.getElementById('averageOpen').value, 10);
const averageExtroverted = parseFloat(document.getElementById('averageExtroverted').value, 10);
const averageStable = parseFloat(document.getElementById('averageStable').value, 10);
const profileName = document.getElementById('profileName').value

const marksCanvas = document.getElementById("marksChart");

const marksData = {
  labels: ["Agreeable", "Conscientious", "Open", "Extroverted", "Stable"],
  datasets: [{
    label: profileName,
    backgroundColor: "rgba(255, 99, 132, 0.2)",  // Fondo del área
    borderColor: "rgba(255, 99, 132, 1)",  // Color del borde
    pointBackgroundColor: "rgba(255, 99, 132, 1)",  // Color de los puntos
    pointBorderColor: "#fff",  // Bordes de los puntos
    pointHoverBackgroundColor: "#fff",  // Color de los puntos al pasar el mouse
    pointHoverBorderColor: "rgba(255, 99, 132, 1)",  // Bordes de los puntos al pasar el mouse
    data: [averageAgreeable, averageConscientious, averageOpen, averageExtroverted, averageStable],
    fontSize: 40,
    borderWidth: 2  // Grosor de las líneas
  }]
};

const radarChart = new Chart(marksCanvas, {
  type: 'radar',
  data: marksData,
  options: {
    responsive: true,
    scale: {
      ticks: {
        beginAtZero: true,  // Comenzar desde 0
        max: 100,  // Límite máximo en el gráfico
        backdropColor: 'rgba(255, 255, 255, 0.1)',  // Fondo detrás de los valores
        fontSize: 12,  // Tamaño de la fuente
        fontColor: 'rgba(0, 0, 0, 0.7)'  // Color de la fuente
      },
      pointLabels: {
        fontSize: 100,  // Aumentar el tamaño de las etiquetas
        fontStyle: 'bold',  // Estilo de la fuente
        fontColor: 'rgba(0, 0, 0, 0.9)'  // Color de las etiquetas
      },
      angleLines: {
        color: 'rgba(128, 128, 128, 0.5)',  // Color de las líneas angulares
        lineWidth: 1  // Grosor de las líneas angulares
      },
      gridLines: {
        color: 'rgba(128, 128, 128, 0.5)',  // Color de las líneas del eje
      }
    },
    legend: {
      display: true,
      position: 'top',  // Colocar la leyenda en la parte superior
      labels: {
        fontColor: '#000',  // Color del texto de la leyenda
        fontSize: 14  // Tamaño de la fuente de la leyenda
      }
    },
    title: {
      display: true,
      text: 'User Personality Profile',
      fontSize: 18,
      fontColor: '#000',
      fontStyle: 'monserrat'
    }
  }
});
