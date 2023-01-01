// any CSS you import will output into a single css file (app.scss in this case)
import './styles/app.scss';

// bootstrap
const bootstrap = require('bootstrap')

// start the Stimulus application
// import './bootstrap';

for (let tooltip of document.querySelectorAll('[data-bs-toggle="tooltip"]')) {
    console.log('jes')
    new bootstrap.Tooltip(tooltip);
}

import './scripts';
