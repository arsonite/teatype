/**
 * @license
 * Copyright (C) 2024-2026 Burak Günaydin
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

const EDGE_PX = 24;
const TAPPABLE = 'a, button, input, select, textarea, label, [role="button"]';

/**
 * Makes a page behave like an app on a phone: no pinch zoom, no double tap zoom, no swipe from the edge to go back.
 * Mobile Safari ignores `user-scalable=no`, so the gestures are stopped here. Returns the function that undoes it.
 */
const lockGestures = (): (() => void) => {
    const stop = (event: Event) => event.preventDefault();
    const onTouchStart = (event: TouchEvent) => {
        const touch = event.touches[0];
        // A finger that starts on the edge is the swipe back (or forward) of the browser, except on a control (the buttons of a rail sit there)
        const onEdge = touch && (touch.clientX < EDGE_PX || touch.clientX > window.innerWidth - EDGE_PX) && !(event.target instanceof Element && event.target.closest(TAPPABLE));
        if (event.touches.length > 1 || onEdge) {
            event.preventDefault();
        }
    };
    const onTouchMove = (event: TouchEvent) => event.touches.length > 1 && event.preventDefault();

    // The back button and the back swipe land on the page itself: the entry that was left is put back
    const holdHistory = () => window.history.pushState(null, '', window.location.href);
    holdHistory();

    const gestures = ['gesturestart', 'gesturechange', 'gestureend'];
    gestures.forEach((name) => document.addEventListener(name, stop, { passive: false }));
    document.addEventListener('touchstart', onTouchStart, { passive: false });
    document.addEventListener('touchmove', onTouchMove, { passive: false });
    window.addEventListener('popstate', holdHistory);

    return () => {
        gestures.forEach((name) => document.removeEventListener(name, stop));
        document.removeEventListener('touchstart', onTouchStart);
        document.removeEventListener('touchmove', onTouchMove);
        window.removeEventListener('popstate', holdHistory);
    };
};

export { lockGestures };
