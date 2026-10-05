// Chapikids Piñatas - JavaScript del carrito

document.addEventListener('DOMContentLoaded', function() {
    // Confirmación al vaciar carrito
    const limpiarForm = document.querySelector('form[action*="limpiar"]');
    if (limpiarForm) {
        limpiarForm.addEventListener('submit', function(e) {
            if (!confirm('¿Estás seguro de que quieres vaciar el carrito?')) {
                e.preventDefault();
            }
        });
    }

    // Validación de cantidad en el carrito
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 0) {
                this.value = 0;
            }
        });
    });
});
