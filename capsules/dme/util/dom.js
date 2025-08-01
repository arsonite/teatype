let main_frame;

let frame_out, out;
let p_old, p_new;

let frame_navigation;
let navUI = {
    left_up: -45,
    up: 0,
    right_up: 45,
    left: -90,
    center: '',
    right: 90,
    left_down: -135,
    down: 180,
    right_down: 135
};

let bodyUI = {
    head: '',
    neck: '',
    chest: '',
    upper_arm_L: '',
    upper_arm_R: '',
    lower_arm_L: '',
    lower_arm_R: '',
    hand_L: '',
    hand_R: '',
    pelvis: '',
    upper_leg_L: '',
    upper_leg_R: '',
    lower_leg_L: '',
    lower_leg_R: '',
    foot_L: '',
    foot_R: ''
};

let armorUI = {
    helmet: ''
};

let frame_enemy;

let stats_window, stats_tab, stats_frame;
let statsWindowOpen = false;
let mind_grid, mind_box;
let health, stamina, grant;
let health_bar, stamina_bar, grant_bar;
let exp, exp_frame, exp_bar;
let profile, attributes1, attributes2;

let status_window, status_tab, status_frame;
let statusWindowOpen = false;

$(document).ready(() => {
    out = id('out');
    p_old = id('old');
    p_new = id('new');

    nav_frame = id('nav_frame');
    enemy_frame = id('enemy_frame');

    stats_window = id('stats_window');
    stats_tab = id('stats_tab');
    stats_frame = id('stats_frame');

    mind_grid = id('mind_grid');
    mind_box = id('mind_box');

    health = id('health');
    stamina = id('stamina');
    grant = id('grant');

    health_bar = id('health_bar');
    stamina_bar = id('stamina_bar');
    grant_bar = id('grant_bar');

    exp = id('exp');
    exp_frame = id('exp_frame');
    exp_bar = id('exp_bar');

    profile = id('profile');
    attributes1 = id('attributes1');
    attributes2 = id('attributes2');

    status_window = id('status_window');
    status_tab = id('status_tab');
    status_frame = id('status_frame');

    appendArrows();
    //appendBody();
    appendGrid();
    appendBars();
    appendXP();

    player.updateGUI_bars();
    player.updateGUI_mind_grid();
    player.updateGUI_profile();
    player.updateGUI_attributes();
    player.updateGUI_XP();

    stats_tab.onclick = () => {
        if (!statsWindowOpen) {
            statsWindowOpen = true;
            stats_window.className = stats_window.className.replace(/_closed/g, '');
            stats_window.className += '_open';
            return;
        }
        statsWindowOpen = false;
        stats_window.className = stats_window.className.replace(/_open/g, '');
        stats_window.className += '_closed';
    };

    status_tab.onclick = () => {
        if (!statusWindowOpen) {
            statusWindowOpen = true;
            status_window.className = status_window.className.replace(/_closed/g, '');
            status_window.className += '_open';
            return;
        }
        statusWindowOpen = false;
        status_window.className = status_window.className.replace(/_open/g, '');
        status_window.className += '_closed';
    };
});

function appendArrows() {
    Object.keys(navUI).forEach(item => {
        let arrow_white = create('img');
        let deg = navUI[item];
        if (deg === '') {
            arrow_white.src = iconURL + 'circle_white.png';
        } else {
            arrow_white.src = iconURL + 'arrow_white.png';
        }
        arrow_white.id = '' + item;

        arrow_white.style.transform = `rotate(${deg}deg)`;

        arrow_white.onclick = () => {
            let string = 'I go ' + item.replace('_', ' ') + '.';
            print(string);
        };

        navUI[item] = arrow_white;
        nav_frame.appendChild(navUI[item]);
    });
}

function appendBody() {
    Object.keys(bodyUI).forEach(item => {
        let svg = readFile(bodyURL, item + '.svg').replace(/\'/g, '');

        enemy_frame.innerHTML += svg;
    });
}

function appendGrid() {
    m = [];
    for (let i = 0; i < 9; i++) {
        let mBox = create('mBox');
        mBox.id = 'm' + i + 1;
        mBox.className = 'mBox';

        let div = create('div');

        let span = create('span');
        span.className = 'tooltip mind';
        div.appendChild(span);

        mBox.onmouseenter = () => {
            span.style.visibility = 'visible';
            span.style.opacity = '1';
        }

        mBox.onmouseleave = () => {
            span.style.visibility = 'hidden';
            span.style.opacity = '0';
        }

        mBox.appendChild(div);

        m.push(mBox);
        mind_grid.appendChild(m[i]);
    }
}

function appendBars() {

}

function appendXP() {
    let div = create('div');
    let span = create('span');

    span.className = 'tooltip xp';
    div.appendChild(span);

    exp_frame.onmouseenter = () => {
        span.style.visibility = 'visible';
        span.style.opacity = '1';
    }

    exp_frame.onmouseleave = () => {
        span.style.visibility = 'hidden';
        span.style.opacity = '0';
    }
    
    exp_frame.appendChild(div);
}
