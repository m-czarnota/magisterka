(function () {
    const forms = document.querySelectorAll('form');
    if (forms.length === 0) {
        return;
    }

    for (let form of forms) {
        form.addEventListener('submit', e => preSubmitValidate(form, e), false);
    }

    function preSubmitValidate(form, event) {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }

        form.classList.add('was-validated')
    }
})();