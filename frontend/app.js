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
const answerDiv = document.getElementById("answer");
const loadingDiv = document.getElementById("loading");

sendBtn.addEventListener("click", async () => {
    const text = questionInput.value.trim();
    
    if (!text) {
        answerDiv.textContent = "Por favor, escribe una pregunta.";
        return;
    }

    // 1. ACTIVAR ESTADO DE CARGA
    if (loadingDiv) loadingDiv.style.display = "flex"; 
    answerDiv.textContent = "";       
    answerDiv.style.opacity = "0.5";

    try {
        // 2. PETICIÓN AL BACKEND
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            // Enviamos 'message' porque así está definido en tu main.py
            body: JSON.stringify({ message: text }), 
        });

        const data = await response.json();

        // 3. DESACTIVAR CARGA Y MOSTRAR RESULTADO
        if (loadingDiv) loadingDiv.style.display = "none";
        answerDiv.style.opacity = "1";

        if (response.ok) {
            // Tu backend devuelve { "answer": "..." }
            answerDiv.textContent = data.answer || "El tutor no ha devuelto texto.";
        } else {
            answerDiv.textContent = "Error en la respuesta del servidor (Status: " + response.status + ")";
        }

    } catch (error) {
        if (loadingDiv) loadingDiv.style.display = "none";
        answerDiv.style.opacity = "1";
        answerDiv.textContent = "No se ha podido conectar con el servidor. Revisa la terminal de Ubuntu.";
        console.error("Error:", error);
    }
});