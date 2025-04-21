// document.addEventListener("DOMContentLoaded", function () {
//     try {
//         const mensajesDataElement = document.getElementById('mensajes-data');
//         if (!mensajesDataElement) {
//             console.error("No se encontró el elemento con id 'mensajes-data'.");
//             return;
//         }

//         const mensajesData = mensajesDataElement.textContent.trim();
//         console.log("Contenido de mensajes-data (antes de parsear):", mensajesData);

//         // Validar si el contenido es un JSON válido
//         let mensajes;
//         try {
//             mensajes = JSON.parse(mensajesData);
//         } catch (jsonError) {
//             console.error("El contenido de mensajes-data no es un JSON válido:", jsonError);
//             return;
//         }

//         console.log("Mensajes procesados (después de parsear):", mensajes);

//         mensajes.forEach(mensaje => {
//             Swal.fire({
//                 icon: mensaje.icono || "info",
//                 title: mensaje.titulo || "Mensaje",
//                 text: mensaje.texto || "",
//                 confirmButtonText: mensaje.boton || "OK"
//             });
//         });
//     } catch (error) {
//         console.error("Error al procesar los mensajes:", error);
//     }
// });