// Validacion si los campos estan vacios
// Validación si los campos están vacíos
document.querySelector('form').onsubmit = function (e) {
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

    // Definición de las tallas y productos
    var productoTallas = {
        'Camisa': ["XL", "S", "M","L","XXL"],
        'Pantalon': ["32", "34", "36","38","40","42","44","46"]
    };

    // Determinación del producto y las tallas válidas
    var producto = nombre.includes('Camisa') ? 'Camisa' :
        nombre.includes('Pantalon') ? 'Pantalon' : null;

    var talasValidas = producto ? productoTallas[producto] : [];

    // Validación del nombre del producto según las tallas del producto
    var isValid = talasValidas.some(function (talla) {
        return nombre.includes(talla);
    });

    // Mensaje de error personalizado para cada producto
    if (!isValid && producto) {
        e.preventDefault(); // Previene el envío del formulario
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: `El nombre del ${producto} debe incluir una de las siguientes tallas: ${talasValidas.join(', ')}`
        });
        return;
    }

};

// No permitir valores negativos ni el singo +
document.querySelector('input[name="precio"]').addEventListener('input', function (e) {
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
document.querySelector('input[name="cantidad"]').addEventListener('input', function (e) {
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
document.querySelector('#precio').addEventListener('input', function (e) {
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