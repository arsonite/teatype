/**
 * @license
 * Copyright (C) 2024-2026 Burak Günaydin
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 */

// React imports
import { useCallback, useEffect, useRef, useState } from 'react';

interface iPointerDrag<T> {
    item: T;
    /** The value of data-drop on the element under the pointer, null over nothing that takes a drop */
    target: string | null;
    x: number;
    y: number;
}

interface iUsePointerDragOptions<T> {
    /** Called when the pointer is released over an element with a data-drop attribute, with the value of it */
    onDrop: (item: T, target: string) => void;
}

const scrollParentOf = (element: HTMLElement): HTMLElement => {
    for (let parent = element.parentElement; parent; parent = parent.parentElement) {
        if (/(auto|scroll)/.test(getComputedStyle(parent).overflowY) && parent.scrollHeight > parent.clientHeight) {
            return parent;
        }
    }
    return document.scrollingElement as HTMLElement;
};

const EDGE = 56; // Distance to the edge of the scrolling area where dragging scrolls it
const SPEED = 14;

/**
 * Drag and drop with pointer events, which works with a finger as well (the HTML5 one does not on a phone). Put
 * `start(item)` on the pointer-down of a handle, the handle needs `touch-action: none` so the page does not scroll
 * instead. Elements that accept the item carry `data-drop="<value>"`, the page scrolls when the pointer is at its
 * edge. The caller draws the dragged item itself, at `drag.x` / `drag.y`.
 */
const usePointerDrag = <T,>({ onDrop }: iUsePointerDragOptions<T>) => {
    const [drag, setDrag] = useState<iPointerDrag<T> | null>(null);
    const dropped = useRef(onDrop);
    const stop = useRef<(() => void) | null>(null);

    useEffect(() => {
        dropped.current = onDrop;
    }, [onDrop]);

    // A drag that is still going on when the component goes away
    useEffect(() => () => stop.current?.(), []);

    const start = useCallback(
        (item: T) => (event: React.PointerEvent<HTMLElement>) => {
            if (event.pointerType === 'mouse' && event.button !== 0) {
                return;
            }
            event.preventDefault();
            stop.current?.();

            const scroller = scrollParentOf(event.currentTarget);
            const userSelect = document.body.style.userSelect;
            document.body.style.userSelect = 'none';
            let [x, y, target] = [event.clientX, event.clientY, null as string | null];
            const update = () => {
                target = document.elementFromPoint(x, y)?.closest<HTMLElement>('[data-drop]')?.dataset.drop ?? null;
                setDrag({ item, target, x, y });
            };
            const move = (moved: PointerEvent) => {
                [x, y] = [moved.clientX, moved.clientY];
                update();
            };
            const scroll = setInterval(() => {
                const area = scroller === document.scrollingElement ? { bottom: window.innerHeight, top: 0 } : scroller.getBoundingClientRect();
                const by = y < area.top + EDGE ? -SPEED : y > area.bottom - EDGE ? SPEED : 0;
                if (by) {
                    scroller.scrollBy(0, by);
                    update();
                }
            }, 16);
            const end = (released: PointerEvent) => {
                finish();
                if (released.type === 'pointerup' && target) {
                    dropped.current(item, target);
                }
            };
            const finish = () => {
                clearInterval(scroll);
                document.body.style.userSelect = userSelect;
                window.removeEventListener('pointermove', move);
                window.removeEventListener('pointerup', end);
                window.removeEventListener('pointercancel', end);
                stop.current = null;
                setDrag(null);
            };

            window.addEventListener('pointermove', move);
            window.addEventListener('pointerup', end);
            window.addEventListener('pointercancel', end);
            stop.current = finish;
            update();
        },
        [],
    );

    return { drag, start };
};

export type { iPointerDrag };
export { usePointerDrag };
