// Dashboard charts and analytics

let weeklyChart = null;

document.addEventListener('DOMContentLoaded', () => {
    loadAnalytics();
    loadAlerts();
    
    // Refresh every 30 seconds
    setInterval(loadAnalytics, 30000);
    
    // Generate report button
    document.getElementById('generateReport').addEventListener('click', generateReport);
});

async function loadAnalytics() {
    try {
        const response = await fetch('/api/get_analytics');
        const data = await response.json();
        
        if (data.success) {
            // Update stats
            document.getElementById('totalStudents').textContent = data.total_students;
            document.getElementById('presentToday').textContent = data.present_today;
            document.getElementById('attendancePercentage').textContent = data.attendance_percentage + '%';
            document.getElementById('lateCount').textContent = data.late_entries.length;
            
            // Update weekly chart
            updateWeeklyChart(data.weekly_data);
            
            // Update most absent students
            updateAbsentList(data.most_absent);
            
            // Update late entries
            updateLateList(data.late_entries);
            
            // Update attendance table
            updateAttendanceTable(data.records);
        }
    } catch (err) {
        console.error('Error loading analytics:', err);
    }
}

function updateWeeklyChart(weeklyData) {
    const ctx = document.getElementById('weeklyChart').getContext('2d');
    
    if (weeklyChart) {
        weeklyChart.destroy();
    }
    
    const labels = weeklyData.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    const values = weeklyData.map(d => d.percentage);
    
    weeklyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Attendance %',
                data: values,
                borderColor: '#5eead4',
                backgroundColor: 'rgba(94, 234, 212, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: '#2dd4bf',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

function updateAbsentList(absentData) {
    const absentList = document.getElementById('absentList');
    
    if (absentData.length === 0) {
        absentList.innerHTML = '<p>No absent data available</p>';
        return;
    }
    
    const html = absentData.map(student => `
        <div class="absent-item">
            <span>${student.name}</span>
            <span style="color: #dc2626; font-weight: 600;">${student.absent_days} days</span>
        </div>
    `).join('');
    
    absentList.innerHTML = html;
}

function updateLateList(lateData) {
    const lateList = document.getElementById('lateList');
    
    if (lateData.length === 0) {
        lateList.innerHTML = '<p>No late entries today</p>';
        return;
    }
    
    const html = lateData.map(entry => `
        <div class="late-item">
            <strong>${entry.name}</strong> arrived at ${entry.time}
        </div>
    `).join('');
    
    lateList.innerHTML = html;
}

function updateAttendanceTable(records) {
    const tableBody = document.getElementById('tableBody');
    
    if (records.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5">No attendance records</td></tr>';
        return;
    }
    
    const html = records.map(record => `
        <tr>
            <td><strong>${record.Name}</strong></td>
            <td>${record.Date}</td>
            <td>${record.Time}</td>
            <td>${record.Emotion}</td>
            <td><span style="color: #059669; font-weight: 600;">${record.Status}</span></td>
        </tr>
    `).join('');
    
    tableBody.innerHTML = html;
}

async function loadAlerts() {
    try {
        const response = await fetch('/api/get_alerts');
        const data = await response.json();
        
        const alertsList = document.getElementById('alertsList');
        
        if (data.success && data.alerts.length > 0) {
            const html = data.alerts.slice(0, 10).map(alert => `
                <div class="alert-item">${alert}</div>
            `).join('');
            alertsList.innerHTML = html;
        } else {
            alertsList.innerHTML = '<p>No alerts</p>';
        }
    } catch (err) {
        console.error('Error loading alerts:', err);
    }
}

async function generateReport() {
    try {
        const today = new Date().toISOString().split('T')[0];
        
        const response = await fetch('/api/generate_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ date: today })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Show report in alert
            alert(result.report);
            showAlert('Report generated successfully!', 'success');
        } else {
            showAlert('Error generating report: ' + result.message, 'error');
        }
    } catch (err) {
        showAlert('Error: ' + err.message, 'error');
    }
}

function showAlert(message, type = 'info') {
    const alert = document.getElementById('alert');
    alert.textContent = message;
    alert.className = `alert ${type} show`;
    
    setTimeout(() => {
        alert.classList.remove('show');
    }, 5000);
}