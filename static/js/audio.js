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

const captureBtn = document.getElementById('captureBtn');

captureBtn.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const chunks = [];
            const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });

            recorder.ondataavailable = e => {
                chunks.push(e.data);
            };

            recorder.onstop = () => {
                const audioBlob = new Blob(chunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio_data', audioBlob);

                // Add CSRF token to form data
                const csrftoken = getCookie('csrftoken');
                formData.append('csrfmiddlewaretoken', csrftoken);

                fetch('/capture-audio/', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        const unp = document.getElementById('output').innerHTML = data.text
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            };

            recorder.start();

            setTimeout(() => {
                recorder.stop();
            }, 5000); // Stop recording after 5 seconds
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
});

function getAllSupportedMimeTypes(...mediaTypes) {
    if (!mediaTypes.length) mediaTypes.push('video', 'audio')
    const CONTAINERS = ['webm', 'ogg', 'mp3', 'mp4', 'x-matroska', '3gpp', '3gpp2', '3gp2', 'quicktime', 'mpeg', 'aac', 'flac', 'x-flac', 'wave', 'wav', 'x-wav', 'x-pn-wav', 'not-supported']
    const CODECS = ['vp9', 'vp9.0', 'vp8', 'vp8.0', 'avc1', 'av1', 'h265', 'h.265', 'h264', 'h.264', 'opus', 'vorbis', 'pcm', 'aac', 'mpeg', 'mp4a', 'rtx', 'red', 'ulpfec', 'g722', 'pcmu', 'pcma', 'cn', 'telephone-event', 'not-supported']
    
    return [...new Set(
      CONTAINERS.flatMap(ext =>
          mediaTypes.flatMap(mediaType => [
            `${mediaType}/${ext}`,
          ]),
      ),
    ), ...new Set(
      CONTAINERS.flatMap(ext =>
        CODECS.flatMap(codec =>
          mediaTypes.flatMap(mediaType => [
            // NOTE: 'codecs:' will always be true (false positive)
            `${mediaType}/${ext};codecs=${codec}`,
          ]),
        ),
      ),
    ), ...new Set(
      CONTAINERS.flatMap(ext =>
        CODECS.flatMap(codec1 =>
        CODECS.flatMap(codec2 =>
          mediaTypes.flatMap(mediaType => [
            `${mediaType}/${ext};codecs="${codec1}, ${codec2}"`,
          ]),
        ),
        ),
      ),
    )].filter(variation => MediaRecorder.isTypeSupported(variation))
  }
  