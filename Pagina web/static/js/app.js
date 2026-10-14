
"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const itemInput = document.getElementById("item");
    const video = document.getElementById("cameraVideo");
    const canvas = document.getElementById("cameraCanvas");
    const startButton = document.getElementById("startCamera");
    const takeButton = document.getElementById("takePhoto");
    const stopButton = document.getElementById("stopCamera");
    const message = document.getElementById("cameraMessage");
    const photoForm = document.getElementById("photoForm");

    let cameraStream = null;
    let isUploading = false;

    if (itemInput && itemInput.form) {
        itemInput.form.addEventListener("submit", (event) => {
            if (!itemInput.value.trim()) {
                event.preventDefault();
                itemInput.value = "";
                itemInput.setCustomValidity(
                    "Escribe un valor antes de apilar."
                );
                itemInput.reportValidity();
            }
        });

        itemInput.addEventListener("input", () => {
            itemInput.setCustomValidity("");
        });
    }

    function showMessage(text, type = "info") {
        message.textContent = text;
        message.className = `alert alert-${type} mt-3 mb-0`;
    }

    function stopCamera() {
        if (cameraStream) {
            cameraStream.getTracks().forEach((track) => track.stop());
            cameraStream = null;
        }

        video.pause();
        video.srcObject = null;
        startButton.disabled = false;
        takeButton.disabled = true;
        stopButton.disabled = true;
    }

    startButton.addEventListener("click", async () => {
        if (!navigator.mediaDevices?.getUserMedia) {
            showMessage(
                "La cámara requiere localhost o una conexión HTTPS.",
                "danger"
            );
            return;
        }

        startButton.disabled = true;
        showMessage("Solicitando permiso para activar la cámara...");

        try {
            // Primero solicita la cámara predeterminada.
            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            });

            video.srcObject = cameraStream;
            video.muted = true;
            video.playsInline = true;

            // Espera hasta que el video tenga dimensiones.
            await new Promise((resolve, reject) => {
                if (video.readyState >= 2 && video.videoWidth > 0) {
                    resolve();
                    return;
                }

                video.onloadedmetadata = () => resolve();
                video.onerror = () => reject(
                    new Error("No se pudo mostrar el video de la cámara.")
                );
            });

            await video.play();

            if (video.videoWidth === 0 || video.videoHeight === 0) {
                throw new Error(
                    "La cámara se conectó, pero no está enviando imagen."
                );
            }

            takeButton.disabled = false;
            stopButton.disabled = false;

            showMessage(
                "Cámara activa. Ya puedes tomar la fotografía.",
                "success"
            );
        } catch (error) {
            stopCamera();

            if (error.name === "NotAllowedError") {
                showMessage(
                    "Permite el acceso a la cámara en la configuración del navegador.",
                    "warning"
                );
            } else if (error.name === "NotFoundError") {
                showMessage(
                    "No se encontró ninguna cámara disponible.",
                    "danger"
                );
            } else if (error.name === "NotReadableError") {
                showMessage(
                    "La cámara está ocupada o no se puede utilizar. Cierra otras aplicaciones que la estén usando.",
                    "danger"
                );
            } else {
                showMessage(
                    error.message ||
                    "No se pudo activar la cámara. Comprueba sus permisos.",
                    "danger"
                );
            }

            console.error("Error de cámara:", error);
        }
    });

    takeButton.addEventListener("click", async () => {
        if (!cameraStream || isUploading) {
            return;
        }

        if (video.videoWidth === 0 || video.videoHeight === 0) {
            showMessage(
                "La cámara no está enviando una imagen. Apágala y vuelve a activarla.",
                "warning"
            );
            return;
        }

        isUploading = true;
        takeButton.disabled = true;
        startButton.disabled = true;
        showMessage("Tomando y guardando fotografía...");

        try {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            const context = canvas.getContext("2d");
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            const blob = await new Promise((resolve) => {
                canvas.toBlob(resolve, "image/jpeg", 0.85);
            });

            if (!blob) {
                throw new Error("No se pudo crear la fotografía.");
            }

            const formData = new FormData();
            formData.append("photo", blob, "captura.jpg");

            const csrfInput = photoForm.querySelector(
                'input[name="csrf_token"]'
            );

            if (!csrfInput) {
                throw new Error("No se encontró el token de seguridad.");
            }

            const response = await fetch("/push-photo", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfInput.value
                },
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.error || "No se pudo apilar la fotografía."
                );
            }

            stopCamera();
            showMessage(result.message, "success");
            window.location.reload();
        } catch (error) {
            showMessage(error.message, "danger");
            takeButton.disabled = false;
            startButton.disabled = false;
            console.error("Error al guardar la fotografía:", error);
        } finally {
            isUploading = false;
        }
    });

    stopButton.addEventListener("click", () => {
        stopCamera();
        showMessage("Cámara apagada.", "secondary");
    });

    window.addEventListener("pagehide", () => {
        if (cameraStream) {
            cameraStream.getTracks().forEach((track) => track.stop());
            cameraStream = null;
        }
    });
});
