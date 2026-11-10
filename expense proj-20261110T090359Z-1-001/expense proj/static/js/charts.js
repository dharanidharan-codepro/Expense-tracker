/**
 * charts.js — Chart.js initialization for Smart Expense Tracker
 * Features:
 *  - Staggered bar entrance animations
 *  - Doughnut rotation and scale animations
 *  - Premium tooltips with rounded glass look
 */

// Modern vibrant color palette for category chart
const CATEGORY_COLORS = [
  '#4f46e5',  // Indigo
  '#06b6d4',  // Cyan
  '#ef4444',  // Coral Red
  '#f59e0b',  // Amber
  '#8b5cf6',  // Purple
  '#10b981',  // Emerald Green
  '#ec4899',  // Pink
  '#64748b',  // Slate Gray
];

/**
 * Initialize the category doughnut chart with high-quality animation.
 */
function initCategoryChart(canvasId, labels, values) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: CATEGORY_COLORS.slice(0, labels.length),
        borderColor: '#ffffff',
        borderWidth: 3,
        hoverBorderWidth: 0,
        hoverOffset: 12,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      cutout: '68%',
      animation: {
        animateRotate: true,
        animateScale: true,
        duration: 1400,
        easing: 'easeOutQuart'
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 16,
            font: { size: 11, family: 'Inter', weight: '600' },
            color: '#475569',
            usePointStyle: true,
            pointStyleWidth: 10,
          }
        },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          titleColor: '#ffffff',
          bodyColor: '#cbd5e1',
          padding: 14,
          cornerRadius: 10,
          boxPadding: 6,
          titleFont: { family: 'Plus Jakarta Sans', weight: '700', size: 13 },
          bodyFont: { family: 'Inter', size: 12 },
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percent = ((context.parsed / total) * 100).toFixed(1);
              return ` ₹${context.parsed.toLocaleString('en-IN', {minimumFractionDigits: 2})} (${percent}%)`;
            }
          }
        }
      }
    }
  });
}

/**
 * Initialize the expense trend bar chart with staggered entrance animation.
 */
function initTrendChart(canvasId, labels, values) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  // Create gradient fill for bar chart
  const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 260);
  gradient.addColorStop(0, 'rgba(79, 70, 229, 0.9)');
  gradient.addColorStop(1, 'rgba(6, 182, 212, 0.25)');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Daily Expenses (₹)',
        data: values,
        backgroundColor: gradient,
        borderColor: 'rgba(79, 70, 229, 1)',
        borderWidth: 0,
        borderRadius: 8,
        borderSkipped: false,
        hoverBackgroundColor: 'rgba(79, 70, 229, 1)',
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 1200,
        easing: 'easeOutQuart',
        delay: function (context) {
          // Stagger effect for bars
          return context.dataIndex * 40;
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          titleColor: '#ffffff',
          bodyColor: '#cbd5e1',
          padding: 14,
          cornerRadius: 10,
          titleFont: { family: 'Plus Jakarta Sans', weight: '700', size: 13 },
          bodyFont: { family: 'Inter', size: 12 },
          callbacks: {
            label: function(context) {
              return ` ₹${context.parsed.y.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            font: { size: 11, family: 'Inter' },
            color: '#94a3b8',
            maxRotation: 45,
          }
        },
        y: {
          grid: { color: 'rgba(226, 232, 240, 0.6)' },
          ticks: {
            font: { size: 11, family: 'Inter' },
            color: '#94a3b8',
            callback: function(value) {
              return '₹' + value.toLocaleString('en-IN');
            }
          },
          beginAtZero: true,
        }
      }
    }
  });
}
