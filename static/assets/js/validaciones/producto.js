// Validacion si los campos estan vacios
 // Validación si los campos están vacíos
 document.querySelector('form').onsubmit = function(e) {
    var inputs = this.querySelectorAll('input');
    var todosLlenos = true; // Asume que todos los campos están llenos

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value === '') {
            todosLlenos = false; // Si un campo está vacío, establece todosLlenos en falso
            break; // No necesitas verificar el resto de los campos, así que puedes salir del bucle
        }
    }

    if (!todosLlenos) {
        e.preventDefault(); // Previene el envío del formulario
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Campos están vacíos'
        });
        return;
    }

    // Validación del nombre del producto
    var nombre = $('#nombre').val();
    var validSizes = ["XL", "S", "M"];
    var isValid = validSizes.some(function(size) {
        return nombre.includes(size);
    });

    if (!isValid) {
        e.preventDefault(); // Previene el envío del formulario
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'El nombre del producto debe incluir una de las siguientes tallas: XL, S, M',
        });
        return;
    }
};

// No permitir valores negativos ni el singo +
document.querySelector('input[name="precio"]').addEventListener('input', function(e) {
    if (this.value < 0 || this.value.includes('+')) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'No se permiten valores negativos!'
        });
        this.value = '';
    }
});

// No permitir valores negativos ni el singo +
document.querySelector('input[name="cantidad"]').addEventListener('input', function(e) {
    if (this.value < 0 || this.value.includes('+')) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'No se permiten valores negativos!'
        });
        this.value = '';
    }
});

// que permita agregar punto en vez de coma al precio de productos
document.querySelector('#precio').addEventListener('input', function(e) {
    var value = this.value;
    var regex = /^\d*\.?\d*$/;

    if (!regex.test(value)) {
        e.preventDefault();
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Por favor, ingresa un número válido. Solo se permiten números y un punto decimal.'
        });
        this.value = value.substr(0, value.length - 1);
    }
});



$(document).ready(function () {
    $('select').select2();
});