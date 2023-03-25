(function () {
    if (!Boolean(document.querySelector('#login-container'))) {
        return;
    }

    const preventsFromValidatingElem = document.querySelector('#prevent-from-validating');
    const usernameElem = document.querySelector('#username');
    const passwordRow = document.querySelector('#password').parentNode;
    const form = document.querySelector('form');

    form.addEventListener('submit', submitEvent);

    async function submitEvent(event)  {
        // TODO: add validate design for empty password on login page
        event.preventDefault();

        if (!passwordRow.classList.contains('d-none')) {
            form.submit();
            return;
        }

        const response = await fetch(Routing.generate('user_check_if_login_with_password'), {
            method: 'POST',
            body: new FormData(form),
        });
        const data = await response.json();
        const hasPassword = data['hasPassword'];

        preventsFromValidatingElem.value = 0;

        if (!hasPassword) {
            form.removeEventListener('submit', submitEvent);
            form.submit();

            return;
        }

        usernameElem.classList.add('disabled');
        passwordRow.classList.remove('d-none');
    }
})();