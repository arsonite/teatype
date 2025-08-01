function print(msg) {
    log(msg);
}

function log(msg, symbol) {
    p_old.innerHTML = p_new.innerHTML + p_old.innerHTML;
    p_new.innerHTML = '';

    if(symbol === undefined) {
        symbol = '';
    }
    
    p_new.innerHTML = symbol + ' ' + msg + '<br>';

    //out.scrollTo(0, out.scrollHeight);
}

function status(js, status) {
    switch (status) {
        case 'ok':
            log( '(*) Finished loading', js + '.');
            break;
    }
}
