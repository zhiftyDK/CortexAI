function speechtotext(base64WavBuffer) {
    return new Promise((resolve, reject) => {
        fetch("http://127.0.0.1:5000/speechtotext", {
            method: "POST",
            body: JSON.stringify({
                audio_data: base64WavBuffer
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            resolve(data.text);
        });
    });
}

function texttospeech(text) {
    return new Promise((resolve, reject) => {
        fetch("http://127.0.0.1:5000/texttospeech", {
            method: "POST",
            body: JSON.stringify({
                text: text
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.blob())
        .then(audiofile => {
            const audioFileObjectURL = URL.createObjectURL(audiofile);
            resolve(audioFileObjectURL);
        });
    });
}

function chat(question) {
    return new Promise((resolve, reject) => {
        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            body: JSON.stringify({
                question: question
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            resolve(data.response);
        });
    });
}

let myvad;
const recordingSymbol = document.getElementById("recording");

async function startVAD() {
    myvad = await vad.MicVAD.new({
        onSpeechStart: () => {
            console.log("Speech start detected")
        },
        onSpeechEnd: async (audio) => {
            myvad.pause();
            recordingSymbol.innerText = "⚫";
            const outputdiv = document.getElementById("outputdiv")
            const wavBuffer = vad.utils.encodeWAV(audio);
            const base64WavBuffer = vad.utils.arrayBufferToBase64(wavBuffer);
            const transcription = await speechtotext(base64WavBuffer);
            console.log("You:", transcription);
            outputdiv.innerHTML += `You: ${transcription}</br>`
            const response = await chat(transcription);
            console.log("Bot:", response);
            outputdiv.innerHTML += `Bot: ${response}</br>`
            const audioFileObjectURL = await texttospeech(response);
            const audioFile = new Audio(audioFileObjectURL);
            const viz = new Visualizer(audioFile, 100, 5, 100, "#000000");
            viz.play();
            viz.addEventListener("ended", () => {
                myvad.start();
                recordingSymbol.innerText = "🔴";
            });
        }
    });
    myvad.start();
    recordingSymbol.innerText = "🔴";
}

function pauseVAD() {
    myvad.pause();
    recordingSymbol.innerText = "⚫";
}