/* Disables any kind of user-based zooming */
let webFrame = require('electron').webFrame;
webFrame.setZoomFactor(1);
webFrame.setVisualZoomLevelLimits(1, 1);
webFrame.setLayoutZoomLevelLimits(0, 0);