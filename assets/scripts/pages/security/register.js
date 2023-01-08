(function () {
    if (!Boolean(document.querySelector('#register-container'))) {
        return;
    }

    const generateButton = document.querySelector('#generate-new-name');
    const submitButton = document.querySelector('button[type="submit"]');

    const spinner = document.querySelector('#generate-name-spinner');
    const usernameInput = document.querySelector('#register_username');

    generateButton.addEventListener('click', async () => {
        submitButton.setAttribute('disabled', 'disabled');
        hideGenerateButton();

        usernameInput.value = await generateNewName();

        showGenerateButton();
        submitButton.removeAttribute('disabled');
    });

    function hideGenerateButton() {
        generateButton.querySelector('i').classList.add('d-none');
        spinner.classList.remove('d-none');
    }

    function showGenerateButton() {
        generateButton.querySelector('i').classList.remove('d-none');
        spinner.classList.add('d-none');
    }

    async function generateNewName() {
        const response = await fetch(Routing.generate('app_generate_name'));
        const data = await response.json();

        return data['name'];
    }
})();