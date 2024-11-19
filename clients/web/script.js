const wakeworddetection = true;
const customwakeword = "cortex";

function wakeword(base64WavBuffer, wakeword) {
    return new Promise((resolve, reject) => {
        fetch("http://127.0.0.1:5000/wakeword", {
            method: "POST",
            body: JSON.stringify({
                audio_data: base64WavBuffer,
                wakeword: wakeword
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            resolve(data.detected);
        });
    });
}

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
let wakeworddetected = false;
const audioElement = document.getElementById("audio");
const viz = new Visualizer(audioElement, 100, 5, 100, "#ffffff");

async function startVAD() {
    myvad = await vad.MicVAD.new({
        onSpeechStart: () => {
            console.log("Speech start detected")
        },
        onSpeechEnd: async (audio) => {
            myvad.pause();
            const wavBuffer = vad.utils.encodeWAV(audio);
            const base64WavBuffer = vad.utils.arrayBufferToBase64(wavBuffer);
            if(wakeworddetected || !wakeworddetection) {
                recordingSymbol.innerText = "⚫";
                const transcription = await speechtotext(base64WavBuffer);
                console.log("You:", transcription);
                const response = await chat(transcription);
                console.log("Bot:", response);
                const audioFileObjectURL = await texttospeech(response);
                audioElement.src = audioFileObjectURL;
                viz.play();
                viz.addEventListener("ended", () => {
                    wakeworddetected = false;
                    myvad.start();
                    if(wakeworddetection) {
                        recordingSymbol.innerText = "🟡";
                    } else {
                        recordingSymbol.innerText = "🔴";
                    }
                });
            }
            if(!wakeworddetected && wakeworddetection) {
                if(await wakeword(base64WavBuffer, customwakeword)) {
                    console.log("Wakeword detected...");
                    wakeworddetected = true;
                    myvad.start();
                    recordingSymbol.innerText = "🔴";
                } else {
                    console.log("Wakeword not detected...");
                    myvad.start();
                }
            }
        }
    });
    myvad.start();
}

startVAD();
if(wakeworddetection) {
    recordingSymbol.innerText = "🟡";
} else {
    recordingSymbol.innerText = "🔴";
}