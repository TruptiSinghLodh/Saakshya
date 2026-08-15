// Camera handling for student registration

let video, canvas, ctx;
let capturedImages = [];
let stream = null;

document.addEventListener('DOMContentLoaded', () => {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    // Load registered students
    loadStudents();
    
    // Event listeners
    document.getElementById('startCamera').addEventListener('click', startCamera);
    document.getElementById('captureBtn').addEventListener('click', captureImage);
    document.getElementById('registerBtn').addEventListener('click', registerStudent);
    document.getElementById('trainBtn').addEventListener('click', trainModel);
});

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 } 
        });
        video.srcObject = stream;
        
        document.getElementById('startCamera').disabled = true;
        document.getElementById('captureBtn').disabled = false;
        
        showAlert('Camera started successfully', 'success');
    } catch (err) {
        showAlert('Error accessing camera: ' + err.message, 'error');
    }
}

function captureImage() {
    const studentName = document.getElementById('studentName').value.trim();
    
    if (!studentName) {
        showAlert('Please enter student name first', 'error');
        return;
    }
    
    if (capturedImages.length >= 15) {
        showAlert('Maximum 15 images captured', 'info');
        return;
    }
    
    // Set canvas size
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    ctx.drawImage(video, 0, 0);
    
    // Get image data
    const imageData = canvas.toDataURL('image/jpeg');
    capturedImages.push(imageData);
    
    // Flash effect
    const overlay = document.getElementById('captureOverlay');
    overlay.style.display = 'block';
    overlay.classList.add('flash');
    
    setTimeout(() => {
        overlay.style.display = 'none';
        overlay.classList.remove('flash');
    }, 300);
    
    // Update progress
    updateProgress();
    
    // Play capture sound (optional)
    // new Audio('capture.mp3').play();
    
    if (capturedImages.length === 15) {
        document.getElementById('captureBtn').disabled = true;
        document.getElementById('registerBtn').disabled = false;
        showAlert('All 15 images captured! Click Register Student', 'success');
    }
}

function updateProgress() {
    const count = capturedImages.length;
    const percentage = (count / 15) * 100;
    
    document.getElementById('progressFill').style.width = percentage + '%';
    document.getElementById('progressText').textContent = `${count} / 15 images captured`;
}

async function registerStudent() {
    const studentName = document.getElementById('studentName').value.trim();
    
    if (!studentName) {
        showAlert('Please enter student name', 'error');
        return;
    }
    
    if (capturedImages.length < 15) {
        showAlert('Please capture at least 15 images', 'error');
        return;
    }
    
    try {
        showAlert('Registering student...', 'info');
        
        const response = await fetch('/api/save_student', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: studentName,
                images: capturedImages
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(result.message, 'success');
            
            // Reset
            capturedImages = [];
            updateProgress();
            document.getElementById('studentName').value = '';
            document.getElementById('registerBtn').disabled = true;
            document.getElementById('captureBtn').disabled = false;
            
            // Reload students list
            loadStudents();
        } else {
            showAlert(result.message, 'error');
        }
    } catch (err) {
        showAlert('Error registering student: ' + err.message, 'error');
    }
}

async function trainModel() {
    try {
        const trainBtn = document.getElementById('trainBtn');
        const trainStatus = document.getElementById('trainStatus');
        
        trainBtn.disabled = true;
        trainStatus.innerHTML = '<div class="status-message">Training model... This may take a few minutes.</div>';
        
        const response = await fetch('/api/train_model', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            trainStatus.innerHTML = `<div class="status-message success">${result.message}</div>`;
            showAlert('Model trained successfully!', 'success');
        } else {
            trainStatus.innerHTML = `<div class="status-message error">${result.message}</div>`;
            showAlert('Training failed: ' + result.message, 'error');
        }
        
        trainBtn.disabled = false;
    } catch (err) {
        const trainStatus = document.getElementById('trainStatus');
        trainStatus.innerHTML = `<div class="status-message error">Error: ${err.message}</div>`;
        showAlert('Training error: ' + err.message, 'error');
        document.getElementById('trainBtn').disabled = false;
    }
}

async function loadStudents() {
    try {
        const response = await fetch('/api/get_students');
        const result = await response.json();
        
        const studentsList = document.getElementById('studentsList');
        
        if (result.success && result.students.length > 0) {
            const studentsHTML = result.students.map(student => 
                `<div class="student-item">${student}</div>`
            ).join('');
            studentsList.innerHTML = studentsHTML;
        } else {
            studentsList.innerHTML = '<p>No students registered yet</p>';
        }
    } catch (err) {
        document.getElementById('studentsList').innerHTML = '<p>Error loading students</p>';
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

// Stop camera when leaving page
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});