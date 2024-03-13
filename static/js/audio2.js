function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const captureBtn2 = document.getElementById('captureBtn2');
const input = document.getElementById('audiofile')
captureBtn2.addEventListener('click', () => {
    const fileInput = document.getElementById('audiofile');
    const file = fileInput.files[0];
    if (!file) {
        console.error('No file selected');
        return;
    }
    
    const formData = new FormData();
    formData.append('audio_data', file);
    
    fetch('/getaudio/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').textContent = data.text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});