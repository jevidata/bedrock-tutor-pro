/*

const sendBtn = document.getElementById("send-btn");
const questionInput = document.getElementById("question");
const answerDiv = document.getElementById("answer");
const loadingDiv = document.getElementById("loading");

sendBtn.addEventListener("click", async () => {
  const question = questionInput.value.trim();
  
  if (!question) {
    answerDiv.textContent = "Por favor, escribe una pregunta.";
    return;
  }

  // 1. Mostrar indicador de carga y limpiar respuesta anterior
  loadingDiv.style.display = "flex";
  answerDiv.textContent = "";
  answerDiv.style.opacity = "0.5";

  try {
    // 2. Llamada al Backend (Asegúrate de que el puerto sea el 8000)
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // Enviamos "question" que es lo que espera tu main.py
      body: JSON.stringify({ question: question }),
    });

    if (!response.ok) {
      throw new Error("Error en la respuesta del servidor");
    }

    const data = await response.json();
    
    // 3. Ocultar indicador y mostrar la respuesta de AWS
    loadingDiv.style.display = "none";
    answerDiv.style.opacity = "1";
    answerDiv.textContent = data.answer || "El tutor no ha encontrado una respuesta específica.";

  } catch (error) {
    // En caso de error, ocultamos el cargando y avisamos
    loadingDiv.style.display = "none";
    answerDiv.style.opacity = "1";
    answerDiv.textContent = "No se ha podido conectar con el backend. Revisa si Uvicorn está corriendo.";
    console.error("Error en la petición:", error);
  }
});
*/
const sendBtn = document.getElementById("send-btn");
const questionInput = document.getElementById("question");
const chatContainer = document.getElementById("answer"); // Usaremos este como contenedor de mensajes
const loadingDiv = document.getElementById("loading");

// Función para añadir mensajes al chat
function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender); // sender será 'user' o 'bot'
    
    const innerDiv = document.createElement("div");
    innerDiv.classList.add("message-content");
    innerDiv.textContent = text;
    
    msgDiv.appendChild(innerDiv);
    chatContainer.appendChild(msgDiv);

    // Auto-scroll hacia abajo para ver la última respuesta
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

sendBtn.addEventListener("click", async () => {
    const text = questionInput.value.trim();
    
    if (!text) return;

    // 1. MOSTRAR MENSAJE DEL USUARIO EN EL CHAT
    appendMessage(text, "user");
    questionInput.value = ""; // Limpiar el input inmediatamente

    // 2. ACTIVAR ESTADO DE CARGA
    if (loadingDiv) loadingDiv.style.display = "flex"; 

    try {
        // 3. PETICIÓN AL BACKEND
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }), 
        });

        const data = await response.json();

        // 4. DESACTIVAR CARGA Y MOSTRAR RESPUESTA DEL BOT
        if (loadingDiv) loadingDiv.style.display = "none";

        if (response.ok) {
            appendMessage(data.answer || "El tutor no ha devuelto texto.", "bot");
        } else {
            appendMessage("Error en la respuesta del servidor (Status: " + response.status + ")", "bot");
        }

    } catch (error) {
        if (loadingDiv) loadingDiv.style.display = "none";
        appendMessage("No se ha podido conectar con el servidor. Revisa la terminal.", "bot");
        console.error("Error:", error);
    }
});

// EXTRA: Enviar con la tecla Enter
questionInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendBtn.click();
    }
});