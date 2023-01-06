(function () {
    const forms = document.querySelectorAll('form');
    if (forms.length === 0) {
        return;
    }

    const events = ['change', 'keyup'];

    for (let form of forms) {
        form.addEventListener('submit', e => preSubmitValidate(form, e));

        const elements = getElementsToValidateFromForm(form);
        for (let element of elements) {
            for (let event of events) {
                element.addEventListener(event, () => elementValidation(element));
            }
        }
    }

    function preSubmitValidate(form, event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            const submitButton = getSubmitElementForForm(form);
            submitButton.classList.add('disabled');
        }

        form.classList.add('was-validated');

        for (let element of getElementsToValidateFromForm(form)) {
            elementValidation(element);
        }
    }

    function elementValidation(element) {
        if (!element.form.classList.contains('was-validated')) {
            return;
        }

        const errorContainer = getErrorContainerForElement(element);
        errorContainer.innerText = element.validity.valid ? null : element.validationMessage;
    }

    function getElementsToValidateFromForm(form) {
        const allowedElements = [HTMLSelectElement, HTMLInputElement];

        return Array.from(form.elements)
            .filter(elem => allowedElements
                .map(allowed => elem instanceof allowed)
                .some(result => result)
            );
    }

    function createErrorContainer() {
        const div = document.createElement('div');
        div.classList.add('invalid-feedback');

        return div;
    }

    function getErrorContainerForElement(element) {
        let errorContainer = element.nextElementSibling;

        if (errorContainer) {
            return errorContainer;
        }

        errorContainer = createErrorContainer();
        element.after(errorContainer);

        return errorContainer;
    }

    function getSubmitElementForForm(form) {
        const elements = Array.from(form.elements);
        const buttons = elements.filter(elem => elem instanceof HTMLButtonElement);

        return buttons.length ? buttons[0] : null;
    }
})();