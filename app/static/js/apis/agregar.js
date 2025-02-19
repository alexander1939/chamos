document.addEventListener('DOMContentLoaded', function () {
    console.log("El script agregar.js se ha cargado correctamente.");  // Verifica que se esté ejecutando

    // Obtener el módulo desde el contexto de Flask
    const modulo = "{{ modulo }}";

    // URL de la API para obtener los datos del formulario
    const apiUrl = `http://localhost:5000/api/catalogo/agregar/?modulo=${modulo}`;

    // Realizar la petición a la API
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener los datos de la API');
            }
            return response.json();
        })
        .then(data => {
            console.log("Datos recibidos de la API:", data);  // Verifica los datos que se reciben

            // Crear el formulario dinámicamente
            const formContainer = document.getElementById('content-container');
            formContainer.innerHTML = '';  // Limpiar cualquier contenido previo

            const form = document.createElement('form');
            form.id = 'agregar-form';
            form.action = "{{ action_url }}";  // La URL de la acción, por ejemplo, "/catalogo/<modulo>/agregar/"
            form.method = 'POST';

            // Crear el campo de "nombre"
            const nombreLabel = document.createElement('label');
            nombreLabel.setAttribute('for', 'nombre');
            nombreLabel.textContent = `Nombre de ${modulo}`;
            form.appendChild(nombreLabel);

            const nombreInput = document.createElement('input');
            nombreInput.type = 'text';
            nombreInput.id = 'nombre';
            nombreInput.name = 'nombre';
            nombreInput.value = data.nombre || '';  // Asignar el valor de la API, si está disponible
            form.appendChild(nombreInput);

            // Crear el campo de "descripción"
            const descripcionLabel = document.createElement('label');
            descripcionLabel.setAttribute('for', 'descripcion');
            descripcionLabel.textContent = `Descripción de ${modulo}`;
            form.appendChild(descripcionLabel);

            const descripcionInput = document.createElement('textarea');
            descripcionInput.id = 'descripcion';
            descripcionInput.name = 'descripcion';
            descripcionInput.value = data.descripcion || '';  // Asignar el valor de la API, si está disponible
            form.appendChild(descripcionInput);

            // Crear el botón de submit
            const submitButton = document.createElement('button');
            submitButton.type = 'submit';
            submitButton.textContent = `Agregar ${modulo}`;
            form.appendChild(submitButton);

            // Insertar el formulario en el contenedor de la página
            formContainer.appendChild(form);

            // Manejar el envío del formulario
            form.addEventListener('submit', async function (event) {
                event.preventDefault();  // Evitar el envío tradicional del formulario

                const formData = new FormData(form);
                const data = {
                    nombre: formData.get('nombre'),
                    descripcion: formData.get('descripcion')
                };

                try {
                    const response = await fetch("{{ action_url }}", {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data),
                        credentials: 'include'  // Incluir cookies para autenticación
                    });

                    if (response.ok) {
                        const result = await response.json();
                        alert("{{ modulo }} agregado correctamente.");
                        window.location.href = `/catalogo/{{ modulo }}`;  // Redirigir después de agregar
                    } else {
                        const error = await response.json();
                        alert(`Error: ${error.error || "Error desconocido"}`);
                    }
                } catch (error) {
                    console.error('Error al enviar el formulario:', error);
                    alert('Hubo un error al enviar el formulario.');
                }
            });
        })
        .catch(error => {
            console.error('Error al obtener datos:', error);
            alert('Error al cargar la información.');
        });
});