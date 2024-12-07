function abrirModal(respuestaId, contenido) {
    document.getElementById('modal').style.display = 'block';
    document.getElementById('fondoModal').style.display = 'block';
    document.getElementById('contenidoModal').value = contenido;

    
    const form = document.getElementById('editarRespuestaForm');
    form.action = `/respuestas/${respuestaId}/editar`;
}

function cerrarModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('fondoModal').style.display = 'none';
}

// Abrir el modal para crear pregunta
function abrirModalPregunta() {
    document.getElementById("modalPregunta").style.display = "block";
    document.getElementById("fondoModal").style.display = "block"; // Mostrar el fondo oscuro
}

// Cerrar el modal
function cerrarModalPregunta() {
    document.getElementById("modalPregunta").style.display = "none";
    document.getElementById("fondoModal").style.display = "none"; // Ocultar el fondo oscuro
}

// Enviar el formulario de nueva pregunta usando AJAX
document.getElementById("formNuevaPregunta").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevenir la recarga de la página
    
    let titulo = document.getElementById("titulo").value;
    let contenido = document.getElementById("contenido").value;
    
    let formData = new FormData();
    formData.append('titulo', titulo);
    formData.append('contenido', contenido);

    fetch('/pregunta', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById("mensajeModalPregunta").innerText = data.message;

            // Si la creación es exitosa, cerramos el modal
            cerrarModalPregunta(); // Asegúrate de cerrar el modal aquí

            // Después de cerrar el modal, redirigir al usuario a la página de preguntas
            window.location.href = '/preguntas';  // Redirigir después de cerrar el modal
        }
    })
    .catch(error => {
        document.getElementById("mensajeModalPregunta").innerText = "Hubo un error al crear la pregunta.";
    });
});

// Cerrar el modal cuando se presiona el botón "Cancelar"
document.getElementById("cancelarPregunta").addEventListener("click", function() {
    cerrarModalPregunta();
});
