// static/charts.js
document.addEventListener("DOMContentLoaded", function(){
  // Category chart
  try {
    const catCanvas = document.getElementById('catChart');
    if (catCanvas && typeof catData !== 'undefined') {
      const labels = Object.keys(catData);
      const vals = Object.values(catData);
      new Chart(catCanvas.getContext('2d'), {
        type: 'pie',
        data: { labels: labels, datasets: [{ data: vals, backgroundColor: ['#4e73df','#1cc88a','#36b9cc','#f6c23e','#e74a3b','#858796'] }] },
        options: { plugins: { legend: { position: 'bottom' } } }
      });
    }

    // Series chart
    const seriesCanvas = document.getElementById('seriesChart');
    if (seriesCanvas && typeof months !== 'undefined') {
      new Chart(seriesCanvas.getContext('2d'), {
        type: 'line',
        data: { labels: months, datasets: [{ label: 'Net (Income - Expense)', data: Object.values(series), fill: true, tension: 0.3, backgroundColor: 'rgba(78,115,223,0.05)', borderColor:'#4e73df' }] },
        options: { scales: { y: { beginAtZero: true } } }
      });
    }
  } catch (e) { console.error(e) }
});
