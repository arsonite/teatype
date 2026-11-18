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
import { useEffect, useRef } from 'react';

// Sync
import type { iLocalStore } from './localStore';

const DEBOUNCE_MS = 250;

/**
 * Keeps values in the local store. Writes wait for a short pause in the changes and only contain the values that
 * changed (by identity, so values are replaced when they change, never mutated), all in one transaction.
 * What is still waiting is written as soon as the page is hidden or closed.
 *
 * @param enabled Nothing is written while false, e.g. until the stored values were read: writing the empty start
 * state would wipe them
 */
const usePersist = (store: iLocalStore, values: Record<string, unknown>, enabled = true): void => {
    const latest = useRef(values);
    const written = useRef<Record<string, unknown>>({});
    // Counts the renders in which a value was replaced, the passed object itself is new on every render
    const version = useRef(0);
    if (Object.keys(values).some((key) => latest.current[key] !== values[key])) {
        version.current++;
    }
    latest.current = values;

    const flush = useRef(() => {});
    flush.current = () => {
        const changed = Object.fromEntries(Object.entries(latest.current).filter(([key, value]) => written.current[key] !== value));
        if (!enabled || !Object.keys(changed).length) {
            return;
        }
        written.current = { ...written.current, ...changed };
        store.write(changed).catch((error) => {
            // Tried again with the next change
            for (const key of Object.keys(changed)) {
                delete written.current[key];
            }
            console.error('Could not save locally', error);
        });
    };

    useEffect(() => {
        const timer = setTimeout(() => flush.current(), DEBOUNCE_MS);
        return () => clearTimeout(timer);
    }, [version.current, enabled]); // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        const onVisibility = () => document.visibilityState === 'hidden' && flush.current();
        const onHide = () => flush.current();
        document.addEventListener('visibilitychange', onVisibility);
        window.addEventListener('pagehide', onHide);
        return () => {
            document.removeEventListener('visibilitychange', onVisibility);
            window.removeEventListener('pagehide', onHide);
        };
    }, []);
};

export { usePersist };
