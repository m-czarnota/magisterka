// any CSS you import will output into a single css file (app.scss in this case)
import './styles/app.scss';

// bootstrap
const bootstrap = require('bootstrap')

// start the Stimulus application
// import './bootstrap';

// start bootstrap turned off components
for (let tooltip of document.querySelectorAll('[data-bs-toggle="tooltip"]')) {
    new bootstrap.Tooltip(tooltip);
}

import './scripts';
import {isMobile} from "./scripts/utils/general/functions";

if (isMobile()) {
    document.querySelector('#mobile-device-danger')?.classList.remove('d-none');
}