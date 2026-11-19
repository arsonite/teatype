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

const SWIPE_PX = 56;

/**
 * Calls `onSwipe` when a finger (or a held mouse button) starts on the left edge and is moved to the right. Returns the
 * function that undoes it.
 */
const edgeSwipe = (onSwipe: () => void): (() => void) => {
    let start: { x: number; y: number } | null = null;
    const begin = (x: number, y: number, target: EventTarget | null) => {
        start = x < EDGE_PX && !(target instanceof Element && target.closest(TAPPABLE)) ? { x, y } : null;
    };
    const move = (x: number, y: number) => {
        if (start && x - start.x > SWIPE_PX && x - start.x > Math.abs(y - start.y)) {
            start = null;
            onSwipe();
        }
    };
    const end = () => {
        start = null;
    };
    const onTouchStart = (event: TouchEvent) => begin(event.touches[0].clientX, event.touches[0].clientY, event.target);
    const onTouchMove = (event: TouchEvent) => move(event.touches[0].clientX, event.touches[0].clientY);
    const onMouseDown = (event: MouseEvent) => begin(event.clientX, event.clientY, event.target);
    const onMouseMove = (event: MouseEvent) => move(event.clientX, event.clientY);

    document.addEventListener('touchstart', onTouchStart, { passive: true });
    document.addEventListener('touchmove', onTouchMove, { passive: true });
    document.addEventListener('touchend', end);
    document.addEventListener('touchcancel', end);
    document.addEventListener('mousedown', onMouseDown);
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', end);

    return () => {
        document.removeEventListener('touchstart', onTouchStart);
        document.removeEventListener('touchmove', onTouchMove);
        document.removeEventListener('touchend', end);
        document.removeEventListener('touchcancel', end);
        document.removeEventListener('mousedown', onMouseDown);
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', end);
    };
};

/**
 * Calls `onSwipe` when a finger (or a held mouse button) is moved to the left, from anywhere on the page. Returns the
 * function that undoes it.
 */
const swipeLeft = (onSwipe: () => void): (() => void) => {
    let start: { x: number; y: number } | null = null;
    const begin = (x: number, y: number) => {
        start = { x, y };
    };
    const move = (x: number, y: number) => {
        if (start && start.x - x > SWIPE_PX && start.x - x > Math.abs(y - start.y) * 1.5) {
            start = null;
            onSwipe();
        }
    };
    const end = () => {
        start = null;
    };
    const onTouchStart = (event: TouchEvent) => begin(event.touches[0].clientX, event.touches[0].clientY);
    const onTouchMove = (event: TouchEvent) => move(event.touches[0].clientX, event.touches[0].clientY);

    document.addEventListener('touchstart', onTouchStart, { passive: true });
    document.addEventListener('touchmove', onTouchMove, { passive: true });
    document.addEventListener('touchend', end);
    document.addEventListener('touchcancel', end);

    return () => {
        document.removeEventListener('touchstart', onTouchStart);
        document.removeEventListener('touchmove', onTouchMove);
        document.removeEventListener('touchend', end);
        document.removeEventListener('touchcancel', end);
    };
};

/**
 * Keeps the page from being scrolled. Safari on iOS scrolls the document when the keyboard opens and, as a home
 * screen app, often leaves it shifted up afterwards: the top of the page hides behind the status bar and an empty
 * strip shows at the bottom. The app scrolls inside its own containers, so any scroll of the window is undone.
 * Returns the function that undoes it.
 */
const pinViewport = (): (() => void) => {
    const reset = () => {
        if (window.scrollX !== 0 || window.scrollY !== 0) {
            window.scrollTo(0, 0);
        }
    };
    // The keyboard animation moves the page for a while after the event
    const resetSoon = () => {
        reset();
        window.setTimeout(reset, 100);
        window.setTimeout(reset, 400);
    };
    const viewport = window.visualViewport;
    window.addEventListener('scroll', reset);
    window.addEventListener('focusout', resetSoon);
    window.addEventListener('orientationchange', resetSoon);
    viewport?.addEventListener('resize', resetSoon);

    return () => {
        window.removeEventListener('scroll', reset);
        window.removeEventListener('focusout', resetSoon);
        window.removeEventListener('orientationchange', resetSoon);
        viewport?.removeEventListener('resize', resetSoon);
    };
};

export { edgeSwipe, lockGestures, pinViewport, swipeLeft };
