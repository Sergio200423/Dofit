document.addEventListener("DOMContentLoaded", function () {
    if (currentPage === "clientes") {
        manejarClientes();
    } else if (currentPage === "productos") {
        manejarProductos();
    }

    function manejarClientes() {

        var form = document.getElementById('registroClientes');
        var alertMessage = document.getElementById('alert-message');
        var modalElement = document.getElementById('modalRegistroClientes');

        if (modalElement) {
            modalElement.addEventListener('show.bs.modal', function () {
                modalElement.removeAttribute('inert');
            });

            modalElement.addEventListener('hide.bs.modal', function () {
                modalElement.setAttribute('inert', '');
            });
        }

        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();

                var formData = new FormData(form);
                var submitButton = document.querySelector('button[type="submit"]');

                submitButton.disabled = true;

                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    form.setAttribute('data-informacion-aceptada', data.InformacionAceptada);
                    if (data.InformacionAceptada) {
                        alertMessage.style.display = 'block';
                        alertMessage.style.color = 'green';
                        alertMessage.textContent = data.message;

                        actualizarListaClientes();
                        form.reset();
                    } else {
                        alertMessage.style.display = 'block';
                        alertMessage.style.color = 'red';
                        alertMessage.textContent = data.message;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alertMessage.style.display = 'block';
                    alertMessage.style.color = 'red';
                    alertMessage.textContent = "Ocurrió un problema al procesar la solicitud. Por favor, inténtalo de nuevo.";
                })
                .finally(() => {
                    submitButton.disabled = false;
                });
            });
        }

        function actualizarListaClientes() {
            fetch('/api/clientes/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Datos recibidos de la API:", data); // Agrega este log para depurar
                if (data.clientes) {
                    const listaClientes = document.getElementById('lista-clientes');
                    listaClientes.innerHTML = '';
        
                    data.clientes.forEach(cliente => {
                        const membresiaActiva = cliente.membresia_activa;
                        const nombreMembresia = membresiaActiva && membresiaActiva.nombreMembresia
                            ? membresiaActiva.nombreMembresia
                            : 'Sin membresía activa';

                        const estadoMembresia = membresiaActiva
                            ? (membresiaActiva.estado === 'activo' ? 'Activo' : 'Inactivo')
                            : 'Inactivo';
                        

                        const badgeClass = membresiaActiva
                            ? (membresiaActiva.estado === 'activo' ? 'badge-success' : 'badge-trashed')
                            : 'badge-trashed';


                        console.log(`Cliente: ${cliente.nombre_cliente}, Estado: ${estadoMembresia}, Clase: ${badgeClass}`); // Depuración

                        const clienteRow = document.createElement('tr');
                        clienteRow.innerHTML = `
                            <td>${cliente.id_cliente}</td>
                            <td>
                                <div class="d-flex align-items-center">
                                    <div class="ms-3">
                                    <p class="fw-bold mb-1">${cliente.nombre_cliente}</p>
                                    </div>
                                </div>
                            </td>
                            <td>${cliente.sexo}</td>
                            <td>${cliente.fecha_nacimiento}</td>
                            <td>${nombreMembresia}</td>
                            <td>
                                <span class="badge ${badgeClass} rounded-pill d-inline">
                                    ${estadoMembresia}
                                </span>
                            </td>
                            <td>
                              <button type="button" class="btn btn-link btn-rounded btn-sm fw-bold">
                                Editar
                              </button>
                            </td>
                        `;
                        listaClientes.appendChild(clienteRow);
                    });
                } else {
                    console.error('No se encontraron clientes.');
                }
            })
            .catch(error => {
                console.error('Error al obtener la lista de clientes:', error);
            });
        }
    }

    function manejarProductos() {
        var form = document.getElementById('registroProductos');
        var alertMessage = document.getElementById('alert-message-productos');
        var modalElement = document.getElementById('ModalRegistroProductos');

        if (modalElement) {
            modalElement.addEventListener('show.bs.modal', function () {
                modalElement.removeAttribute('inert');
            });

            modalElement.addEventListener('hide.bs.modal', function () {
                modalElement.setAttribute('inert', '');
            });
        }

        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();

                var formData = new FormData(form);
                var submitButton = document.querySelector('button[type="submit"]');

                submitButton.disabled = true;

                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    form.setAttribute('data-informacion-aceptada', data.InformacionValida);
                    if (data.InformacionValida) {
                        alertMessage.style.display = 'block';
                        alertMessage.style.color = 'green';
                        alertMessage.textContent = data.message;

                        actualizarListaProductos();
                        form.reset();
                    } else {
                        alertMessage.style.display = 'block';
                        alertMessage.style.color = 'red';
                        alertMessage.textContent = data.message;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alertMessage.style.display = 'block';
                    alertMessage.style.color = 'red';
                    alertMessage.textContent = "Ocurrió un problema al procesar la solicitud. Por favor, inténtalo de nuevo.";
                })
                .finally(() => {
                    submitButton.disabled = false;
                });
            });
        }

        function actualizarListaProductos() {
            fetch('/api/productos/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.productos) {
                    const listaProductos = document.getElementById('lista-productos');
                    listaProductos.innerHTML = '';

                    data.productos.forEach(producto => {
                        const productoRow = document.createElement('tr');
                        productoRow.innerHTML = `
                            <td>${producto.id}</td>
                            <td>${producto.nombre_producto}</td>
                            <td>${producto.precio}</td>
                            <td>${producto.existencia}</td>
                            <td>${producto.tipo}</td>
                            <td>${producto.estado}</td>
                            <td>
                              <button type="button" class="btn btn-link btn-rounded btn-sm fw-bold">
                                Editar
                              </button>
                            </td>
                        `;
                        listaProductos.appendChild(productoRow);
                    });
                } else {
                    console.error('No se encontraron productos.');
                }
            })
            .catch(error => {
                console.error('Error al obtener la lista de productos:', error);
            });
        }
    }
});