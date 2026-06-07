# HTML/JS component for Web Speech API
VOICE_INPUT_HTML = """
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px; font-family: sans-serif;">
    <button id="recordBtn" style="padding: 10px 20px; border-radius: 20px; background: #6C63FF; color: white; border: none; cursor: pointer; font-weight: bold;">
        🎤 Start Voice Input
    </button>
    <p id="status" style="font-size: 12px; color: #888;">Click the button to speak</p>
    <textarea id="output" style="width: 100%; height: 60px; border: 1px solid #ddd; border-radius: 5px; padding: 5px;"></textarea>
</div>

<script>
    const recordBtn = document.getElementById('recordBtn');
    const status = document.getElementById('status');
    const output = document.getElementById('output');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        status.innerText = "Speech Recognition not supported in this browser.";
        recordBtn.disabled = true;
    } else {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            status.innerText = "Listening...";
            recordBtn.style.background = "#FF4B4B";
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            output.value = transcript;
            status.innerText = "Speech captured!";
            recordBtn.style.background = "#6C63FF";

            // Send result back to Streamlit via window.parent.postMessage
            window.parent.postMessage({
                type: 'streamlit:set_component_value',
                value: transcript
            }, '*');
        };

        recognition.onerror = (event) => {
            status.innerText = "Error: " + event.error;
            recordBtn.style.background = "#6C63FF";
        };

        recognition.onend = () => {
            status.innerText = "Click the button to speak";
            recordBtn.style.background = "#6C63FF";
        };

        recordBtn.onclick = () => recognition.start();
    }
</script>
"""

def render_voice_button():
    """
    Helper to wrap the HTML for streamlit.components.v1.html
    """
    import streamlit.components.v1 as components
    components.html(VOICE_INPUT_HTML, height=200)
