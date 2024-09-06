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
