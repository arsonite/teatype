/* Alert-Div containers */
let alertError = document.createElement('div');
alertError.className = 'alert';
alertError.id = 'error';
alertError.onclick = () => {
    alertClick(alertError);
};

let alertInfo = document.createElement('div');
alertInfo.className = 'alert';
alertInfo.id = 'info';
alertInfo.onclick = () => {
    alertClick(alertInfo);
};

let alertSuccess = document.createElement('div');
alertSuccess.className = 'alert';
alertSuccess.id = 'success';
alertSuccess.onclick = () => {
    alertClick(alertSuccess);
};

let alertWarning = document.createElement('div');
alertWarning.className = 'alert';
alertWarning.id = 'warning';
alertWarning.onclick = () => {
    alertClick(alertWarning);
};

/* onClick-Functionality for alerts */
function alertClick(alert) {
    new Audio(sfxURL + 'multi_click_2.mp3').play();
    alert.style.display = 'none';
}

function alert(type, msg) {
    switch (type) {
        case 'error':
            new Audio(sfxURL + 'alert_error.wav').play();
            createAlert(alertError, msg);
            break;
        case 'info':
            new Audio(sfxURL + 'alert_info.wav').play();
            createAlert(alertInfo, msg);
            break;
        case 'success':
            new Audio(sfxURL + 'alert_success.wav').play();
            createAlert(alertSuccess, msg);
            break;
        case 'warning':
            new Audio(sfxURL + 'alert_warning.wav').play();
            createAlert(alertWarning, msg);
            break;
    }
}

function createAlert(alert, msg) {
    alert.innerHTML = '<strong>' + alert.id.toUpperCase() + '</strong> ' + msg;

    if (alert.style.display === 'none') {
        alert.style.display = 'block';
        return;
    }
    alerts.appendChild(alert);
}
