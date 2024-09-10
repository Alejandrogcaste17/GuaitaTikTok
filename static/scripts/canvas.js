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

const totalVideos = parseInt(document.getElementById('cursor').value, 10);; // Número total de videos (puedes cargar este valor dinámicamente)
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
            backgroundColor: ['#28a745', '#6c757d'], // Verde para videos almacenados, gris para videos restantes
            hoverBackgroundColor: ['#218838', '#5a6268'], // Colores de hover
            borderWidth: 1,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%', // Hace que sea un gráfico tipo doughnut con un corte en el centro
        plugins: {
            legend: {
                display: false // Ocultar leyenda si no es necesaria
            }
        },
        animation: {
            animateRotate: true, // Animación rotativa
            duration: 2000, // Duración de la animación (2 segundos)
            easing: 'easeInOutCubic' // Efecto de suavizado
        }
    }
});

const ctx = document.getElementById('videoChart').getContext('2d');

// Crear el gráfico circular (doughnut)
const videoChart = new Chart(ctx, {
    type: 'doughnut', // Gráfico circular de tipo 'doughnut'
    data: {
        labels: ['Number of classified videos', 'Videos found without transcription to text'],
        datasets: [{
            data: [classifiedVideos, totalVideos - classifiedVideos],
            backgroundColor: ['#28a745', '#6c757d'], // Verde para videos almacenados, gris para videos restantes
            hoverBackgroundColor: ['#218838', '#5a6268'], // Colores de hover
            borderWidth: 1,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%', // Hace que sea un gráfico tipo doughnut con un corte en el centro
        plugins: {
            legend: {
                display: false // Ocultar leyenda si no es necesaria
            }
        },
        animation: {
            animateRotate: true, // Animación rotativa
            duration: 2000, // Duración de la animación (2 segundos)
            easing: 'easeInOutCubic' // Efecto de suavizado
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
    console.log(listDays)
    
    const listWeeksString = document.getElementById('listWeeks').value;
    const listWeeks = JSON.parse(listWeeksString);
    console.log(listDays)

    const listMonthsString = document.getElementById('listMonths').value;
    const listMonths = JSON.parse(listMonthsString);
    console.log(listDays)

    // Extraer las etiquetas y datos de cada división
    const daysLabels = [];
    const daysVideosCounts = [];

    // Recorre la lista de días
    listDays.forEach(dayEntry => {
        // Almacena el label (día)
        daysLabels.push(dayEntry.day);

        // Almacena la cantidad de videos en list_videos
        daysVideosCounts.push(dayEntry.list_videos.length);
    });

    const weeksLabels = [];
    const weeksVideosCounts = [];

    // Recorre la lista de semanas
    listWeeks.forEach(weekEntry => {
        // Almacena el label (semanas)
        weeksLabels.push(weekEntry.week_start);

        // Almacena la cantidad de videos en list_videos
        weeksVideosCounts.push(weekEntry.list_videos.length);
    });

    const monthsLabels = [];
    const monthsVideosCounts = [];

    // Recorre la lista de meses
    listMonths.forEach(monthEntry => {
        // Almacena el label (meses)
        monthsLabels.push(monthEntry.month);

        // Almacena la cantidad de videos en list_videos
        monthsVideosCounts.push(monthEntry.list_videos.length);
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
    let totalValue = data.values.reduce((acc, val) => acc + val, 0);
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

const ctx9 = document.getElementById('myLineChart').getContext('2d');

    const myLineChart = new Chart(ctx9, {
        type: 'line', // Tipo de gráfico
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'], // Las etiquetas del eje X
            datasets: [
                {
                    label: 'Agressiveness',
                    data: [10, 30, 50, 20, 25, 44, 60], // Datos de la primera línea
                    borderColor: 'rgba(255, 99, 132, 1)', // Color de la línea
                    backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo de los puntos
                    borderWidth: 1, // Grosor de la línea
                    pointStyle: 'circle', // Estilo de los puntos
                    pointRadius: 5, // Tamaño de los puntos
                    fill: false // No rellenar debajo de la línea
                },
                {
                    label: 'Argumentative',
                    data: [20, 40, 35, 50, 40, 70, 90], // Datos de la segunda línea
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderWidth: 1,
                    pointStyle: 'rect', // Estilo de los puntos (cuadrados)
                    pointRadius: 5,
                    fill: false
                },
                {
                    label: 'Offensiveness',
                    data: [30, 50, 45, 60, 50, 80, 100], // Datos de la tercera línea
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 1,
                    pointStyle: 'triangle', // Estilo de los puntos (triángulos)
                    pointRadius: 5,
                    fill: false
                },
                {
                    label: 'Constructiveness',
                    data: [40, 60, 55, 70, 60, 90, 110], // Datos de la cuarta línea
                    borderColor: 'rgba(153, 102, 255, 1)',
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderWidth: 1,
                    pointStyle: 'rectRot', // Estilo de los puntos (rectángulos rotados)
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


function drawFace(humor) {
    const canvas = document.getElementById('humorCanvas');
    const ctx = canvas.getContext('2d');

    // Limpiar el canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Dibujar la cara
    // Dibuja el círculo exterior de la cara (fondo sin relleno)
    ctx.beginPath();
    ctx.arc(100, 100, 80, 0, Math.PI * 2, true); // Círculo exterior
    ctx.lineWidth = 5;
    ctx.strokeStyle = '#000000';
    ctx.stroke();

    // Crear una máscara circular
    ctx.save();  // Guardar el contexto actual
    ctx.beginPath();
    ctx.arc(100, 100, 80, 0, Math.PI * 2, true);  // Definir el área circular
    ctx.clip();  // Aplicar la máscara circular

    // Calcular el relleno en función del valor de humor
    const fillHeight = 160 * humor; // Proporcional al valor de humor (0.0 - 1.0)
    ctx.fillStyle = 'yellow';
    ctx.fillRect(20, 180 - fillHeight, 160, fillHeight);  // Rellenar desde la parte inferior

    ctx.restore();  // Restaurar el contexto sin el clip

    // Dibuja los ojos
    ctx.beginPath();
    ctx.arc(70, 80, 10, 0, Math.PI * 2, true);  // Ojo izquierdo
    ctx.arc(130, 80, 10, 0, Math.PI * 2, true); // Ojo derecho
    ctx.fillStyle = '#000000';
    ctx.fill();

    // Dibuja la boca sonriente
    ctx.beginPath();
    ctx.arc(100, 130, 50, 0, Math.PI, false);  // Boca (arco)
    ctx.lineWidth = 5;
    ctx.stroke();
}

// Valor fijo de humor (valor entre 0.0 y 1.0)
const humorLevel = 0.75;

// Mostrar el valor de humor
document.getElementById('humorValue').innerText = humorLevel.toFixed(2);

// Llamar a la función para dibujar la cara y el relleno según el humor
drawFace(humorLevel);

// Mostrar un label cuando el ratón esté sobre el canvas
const canvas = document.getElementById('humorCanvas');
const hoverLabel = document.getElementById('hoverLabel');

canvas.addEventListener('mousemove', function(event) {
    // Mostrar el valor de humor en la etiqueta
    hoverLabel.innerText = `Humor: ${humorLevel.toFixed(2)}`;
    hoverLabel.style.visibility = 'visible';

    // Posicionar la etiqueta justo donde está el ratón
    hoverLabel.style.top = event.clientY + 'px'; // Posición Y exacta del ratón
    hoverLabel.style.left = event.clientX + 'px'; // Posición X exacta del ratón
});

// Ocultar la etiqueta cuando el ratón sale del canvas
canvas.addEventListener('mouseout', function() {
    hoverLabel.style.visibility = 'hidden';
});

const ctx5 = document.getElementById('profileChart').getContext('2d');

const averageAgreeable = parseFloat(document.getElementById('averageAgreeable').value, 10);
const averageConscientious = parseFloat(document.getElementById('averageConscientious').value, 10);
const averageOpen = parseFloat(document.getElementById('averageOpen').value, 10);
const averageExtroverted = parseFloat(document.getElementById('averageExtroverted').value, 10);
const averageStable = parseFloat(document.getElementById('averageStable').value, 10);

// Datos del gráfico (ejemplo de porcentajes)
const data = {
    labels: ['Agreeable', 'Conscientious', 'Open', 'Extroverted', 'Stable'],
    values: [averageAgreeable, averageConscientious, averageOpen, averageExtroverted, averageStable],  // Sumarán el 100%
    colors: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#1abc9c']
};

// Función para dibujar el gráfico de quesitos
function drawPieChart(ctx5, data) {
    let totalValue = data.values.reduce((acc, val) => acc + val, 0);
    let startAngle = 0;

    data.values.forEach((value, index) => {
        let formattedValue = parseFloat(value.toFixed(2));
        let sliceAngle = (formattedValue / totalValue) * 2 * Math.PI;
        ctx5.beginPath();
        ctx5.moveTo(200, 200);  // Punto central del gráfico (x, y)
        ctx5.arc(200, 200, 150, startAngle, startAngle + sliceAngle);  // Dibujar el sector
        ctx5.closePath();

        // Rellenar el sector con su color correspondiente
        ctx5.fillStyle = data.colors[index];
        ctx5.fill();

        // Calcular la posición para el label (en el centro de cada porción)
        let middleAngle = startAngle + sliceAngle / 2;
        let labelX = 200 + (Math.cos(middleAngle) * 100);  // Coordenada X del label
        let labelY = 200 + (Math.sin(middleAngle) * 100);  // Coordenada Y del label

        // Dibujar el texto (label) en el gráfico
        ctx5.fillStyle = "#000";  // Color del texto
        ctx5.font = "16px Arial";  // Estilo de la fuente
        ctx5.textAlign = "center";  // Alinear el texto
        ctx5.fillText(`${formattedValue}%`, labelX, labelY);  // Dibujar el label

        // Actualizar el ángulo de inicio para el siguiente sector
        startAngle += sliceAngle;
    });
}

// Llamada a la función para dibujar el gráfico
drawPieChart(ctx5, data);
