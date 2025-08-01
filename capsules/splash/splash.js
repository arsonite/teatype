$(document).ready(() => {
  /* Parses the video from the DOM and plays it */
  let video = $('#unlock')[0];

  if (splash_boolean === 'true') {
    $('#splash')[0].style.display = 'none';
    $('#bars')[0].style.display = 'none';

    body.style.overflowY = true;
    body.style.background = '#222';

    nav.style.display = 'flex';
    main.style.display = 'block';
    bg.style.display = 'block';
    footer.style.display = 'flex';

    video.style.display = 'none';

    return;
  }

  let frame_in = $('#frame_in')[0];
  let frame_key = $('#frame_key')[0];

  let upper_bar = $('#upper_bar')[0];
  let lower_bar = $('#lower_bar')[0];

  let white_key = $('#white_key')[0];
  let orange_key = $('#orange_key')[0];

  splash.style.display = 'block';

  nav.style.display = 'none';
  main.style.display = 'none';
  bg.style.display = 'none';
  footer.style.display = 'none';

  white_key.onmouseenter = () => {
    orange_key.style.display = 'block';
    white_key.style.display = 'none';
    new Audio('res/sfx/key_jangle.wav').play();
  };

  orange_key.onmouseleave = () => {
    orange_key.style.display = 'none';
    white_key.style.display = 'block';
  };

  /* After the video ended, launch the main (and only) HTML */
  video.addEventListener('ended', () => {
    video.style.display = 'none';
    $('#bars')[0].style.display = 'flex';

    setTimeout(() => {
      upper_bar.className = 'move';
      lower_bar.className = 'move';

      new Audio('res/sfx/slide_door.wav').play();

      body.style.overflowY = true;
      body.style.background = '#222';

      nav.style.display = 'flex';
      main.style.display = 'block';
      bg.style.display = 'block';
      footer.style.display = 'flex';

      writeFile(dbURL, 'splash_boolean', 'txt', 'true');
    }, 100);
  });

  orange_key.onclick = () => {
    new Audio('res/sfx/click.mp3').play();
    video.play();
    frame_in.style.display = 'none';
    frame_key.style.display = 'none';
  };

  $('form').keypress(function(e) {
    if (e.which == 13) {
      return false;
    }
  });
});
