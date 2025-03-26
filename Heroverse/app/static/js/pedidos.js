document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const searchInput = document.getElementById('orderSearch');
    const searchButton = document.querySelector('.search-box button');
    const statusFilter = document.getElementById('statusFilter');
    const orderRows = document.querySelectorAll('.order-row');
    
    // Función para filtrar pedidos por texto de búsqueda
    function filterBySearch() {
        const searchText = searchInput.value.toLowerCase();
        
        orderRows.forEach(row => {
            const orderId = row.querySelector('.order-id').textContent.toLowerCase();
            const customerName = row.querySelector('.customer-name').textContent.toLowerCase();
            const products = row.querySelector('.products-list').textContent.toLowerCase();
            
            if (orderId.includes(searchText) || 
                customerName.includes(searchText) || 
                products.includes(searchText)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    
    // Función para filtrar pedidos por estado
    function filterByStatus() {
        const selectedStatus = statusFilter.value.toLowerCase();
        
        orderRows.forEach(row => {
            // Si no hay filtro seleccionado, mostrar todas las filas
            if (!selectedStatus) {
                row.style.display = '';
                return;
            }
            
            const rowStatus = row.querySelector('.status-badge').textContent.toLowerCase();
            
            // Mostrar fila si coincide con el estado seleccionado
            if (rowStatus === selectedStatus) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    
    // Función para aplicar ambos filtros
    function applyFilters() {
        orderRows.forEach(row => {
            row.style.display = '';
        });
        
        // Aplicar filtros en secuencia
        filterBySearch();
        filterByStatus();
    }
    
    // Event listeners
    searchButton.addEventListener('click', applyFilters);
    
    searchInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            applyFilters();
        }
    });
    
    // Filtrar cuando cambia el selector de estado
    statusFilter.addEventListener('change', applyFilters);
    
    // Configurar los botones de acción
    const viewButtons = document.querySelectorAll('.view-button');
    const editButtons = document.querySelectorAll('.edit-button');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!this.getAttribute('href') || this.getAttribute('href') === '#') {
                event.preventDefault();
                const orderId = this.closest('tr').querySelector('.order-id').textContent.trim().replace('#', '');
                window.location.href = `/pedidos/${orderId}`;
            }
        });
    });
    
    editButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!this.getAttribute('href') || this.getAttribute('href') === '#') {
                event.preventDefault();
                const orderId = this.closest('tr').querySelector('.order-id').textContent.trim().replace('#', '');
                window.location.href = `/pedidos/${orderId}/editar`;
            }
        });
    });
});