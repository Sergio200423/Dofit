// filtrarProducto.js
// Este script hace que los filtros de productos sean dinámicos usando fetch y actualiza la tabla y los contadores sin recargar la página.
document.addEventListener('DOMContentLoaded', function() {
    console.log('[DEBUG] filtrarProducto.js cargado correctamente');
    const form = document.getElementById('filtro-productos-form');
    const nombreInput = document.getElementById('nombre');
    // Checkbox de tipo
    const tipoCheckboxes = document.querySelectorAll('input[name="tipo"]');
    // Checkbox de estado
    const estadoCheckboxes = document.querySelectorAll('input[name="estado"]');
    // Tabla de productos
    const tbody = document.getElementById('lista-productos');
    // Contadores de pills (selección robusta según estructura de productos.html)
    const contadorTotal = document.querySelector('#tipoTodos')?.parentElement.querySelector('.contador');
    const contadorBarraEnergetica = document.querySelector('#tipoBarraEnergetica')?.parentElement.querySelector('.contador');
    const contadorProteina = document.querySelector('#tipoProteina')?.parentElement.querySelector('.contador');
    const contadorVitaminas = document.querySelector('#tipoVitaminas')?.parentElement.querySelector('.contador');
    const contadorSuplementos = document.querySelector('#tipoSuplementos')?.parentElement.querySelector('.contador');
    const contadorBebidas = document.querySelector('#tipoBebidas')?.parentElement.querySelector('.contador');
    const contadorCaramelos = document.querySelector('#tipoCaramelos')?.parentElement.querySelector('.contador');
    // Estado: los contadores están en el mismo orden que los labels de estado
    const estadoContadores = Array.from(estadoCheckboxes).map(cb => cb.parentElement.querySelector('.contador'));

    // Manejar cambios en los filtros
    function attachListeners() {
        nombreInput && nombreInput.addEventListener('input', filtrarProductos);
        tipoCheckboxes.forEach(cb => cb.addEventListener('change', () => {
            toggleActivePill(cb);
            mostrarFiltrosAplicados();
            filtrarProductos();
        }));
        estadoCheckboxes.forEach(cb => cb.addEventListener('change', () => {
            toggleActivePill(cb);
            mostrarFiltrosAplicados();
            filtrarProductos();
        }));
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                mostrarFiltrosAplicados();
                filtrarProductos();
            });
        }
    }

    // Activa/desactiva la clase .active en el label del filtro
    function toggleActivePill(checkbox) {
        const label = checkbox.parentElement;
        if (checkbox.checked) {
            label.classList.add('active');
        } else {
            label.classList.remove('active');
        }
    }

    // Muestra los filtros aplicados debajo de los pills
    function mostrarFiltrosAplicados() {
        const contenedor = document.getElementById('filtros-aplicados-container');
        if (!contenedor) return;
        const seleccionados = [];
        tipoCheckboxes.forEach(cb => {
            if (cb.checked && cb.value !== 'Todos') { // Elimina el filtro 'Todos' de la visualización
                const label = cb.parentElement.textContent.trim().split('\n')[0].trim();
                seleccionados.push(label);
            }
        });
        estadoCheckboxes.forEach(cb => {
            if (cb.checked) {
                const label = cb.parentElement.textContent.trim().split('\n')[0].trim();
                seleccionados.push(label);
            }
        });
        if (nombreInput && nombreInput.value.trim() !== '') {
            seleccionados.push('Nombre: ' + nombreInput.value.trim());
        }
        // Limpiar y mostrar
        contenedor.innerHTML = '<span class="filtros-aplicadas-label">Filtros aplicados:</span> ';
        if (seleccionados.length > 0) {
            contenedor.style.display = '';
            seleccionados.forEach(filtro => {
                const span = document.createElement('span');
                span.className = 'filtro-aplicado';
                span.textContent = filtro;
                contenedor.appendChild(span);
            });
        } else {
            contenedor.style.display = 'none';
        }
    }

    function getSelectedValues(nodelist) {
        return Array.from(nodelist).filter(cb => cb.checked).map(cb => cb.value);
    }

    function filtrarProductos() {
        const tipos = getSelectedValues(tipoCheckboxes);
        const estados = getSelectedValues(estadoCheckboxes);
        const nombre = nombreInput ? nombreInput.value : '';
        console.log('[DEBUG] Filtros enviados:', { tipos, estados, nombre });
        fetch('/productos/filtrar_producto/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                tipo: tipos,
                estado: estados,
                nombre: nombre
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('[DEBUG] Respuesta de filtrar_producto:', data);
            actualizarTablaProductos(data.productos);
            actualizarContadores(data);
        })
        .catch(error => {
            console.error('Error al filtrar productos:', error);
        });
    }

    function actualizarTablaProductos(productos) {
        if (!tbody) return;
        tbody.innerHTML = '';
        if (!productos || productos.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center py-4"><p class="mb-0 text-muted">No hay productos registrados</p></td></tr>`;
            return;
        }
        productos.forEach(producto => {
            // Determinar estado visual según existencia
            let estadoVisual = '';
            if (producto.existencia === 0) {
                estadoVisual = 'agotado';
            } else {
                estadoVisual = 'disponible';
            }
            const tr = document.createElement('tr');
            tr.setAttribute('data-producto-id', producto.id_producto);
            tr.innerHTML = `
                <td><div class="producto-imagen">${producto.imagen ? `<img src="${producto.imagen}" alt="${producto.nombre_producto}" class="img-thumbnail">` : `<img src="/static/img/placeholder.jpg" alt="Sin imagen" class="img-thumbnail">`}</div></td>
                <td><div class="d-flex align-items-center"><div class="ms-3"><p class="fw-bold mb-1">${producto.nombre_producto}</p></div></div></td>
                <td>$${producto.precio}</td>
                <td><p class="descripcion-producto">${producto.descripcion ? producto.descripcion.substring(0, 50) : ''}</p></td>
                <td>${producto.existencia} unidades</td>
                <td>${producto.tipo}</td>
                <td>${renderEstadoBadge(estadoVisual)}</td>
                <td><button class="btn btn-link btn-rounded btn-sm fw-bold editar-producto-btn" data-id="${producto.id_producto}"><i class="fas fa-edit"></i> Editar</button></td>
            `;
            tbody.appendChild(tr);
        });
    }

    // Renderiza el badge de estado (solo disponible/agotado)
    function renderEstadoBadge(estado) {
        if (!estado) return '';
        let badgeClass = '';
        let label = '';
        if (estado === 'disponible') {
            badgeClass = 'badge-success';
            label = 'Disponible';
        } else if (estado === 'agotado') {
            badgeClass = 'badge-trashed';
            label = 'Agotado';
        }
        return `<span class="badge ${badgeClass} rounded-pill d-inline">${label}</span>`;
    }

    function actualizarContadores(data) {
        if (contadorBarraEnergetica) contadorBarraEnergetica.textContent = data.barra_energetica_count ?? 0;
        if (contadorTotal) contadorTotal.textContent = data.total_productos ?? 0;
        if (contadorProteina) contadorProteina.textContent = data.tipo_counts && data.tipo_counts.Proteina ? data.tipo_counts.Proteina : 0;
        if (contadorVitaminas) contadorVitaminas.textContent = data.tipo_counts && data.tipo_counts.Vitaminas ? data.tipo_counts.Vitaminas : 0;
        if (contadorSuplementos) contadorSuplementos.textContent = data.tipo_counts && data.tipo_counts.Suplementos ? data.tipo_counts.Suplementos : 0;
        if (contadorBebidas) contadorBebidas.textContent = data.tipo_counts && data.tipo_counts.Bebidas ? data.tipo_counts.Bebidas : 0;
        if (contadorCaramelos) contadorCaramelos.textContent = data.tipo_counts && data.tipo_counts.Caramelos ? data.tipo_counts.Caramelos : 0;
        // Estado: actualiza los contadores de estado
        if (data.estados_conteo && estadoContadores.length === data.estados_conteo.length) {
            data.estados_conteo.forEach((estado, idx) => {
                if (estadoContadores[idx]) estadoContadores[idx].textContent = estado[2] ?? 0;
            });
        }
    }

    // Utilidad para CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    attachListeners();
    // Inicializa el estado visual de los pills y los filtros aplicados al cargar
    tipoCheckboxes.forEach(cb => toggleActivePill(cb));
    estadoCheckboxes.forEach(cb => toggleActivePill(cb));
    mostrarFiltrosAplicados();
});
