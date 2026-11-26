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
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

// Sync
import { findDirty, hashOf, syncCollection } from './engine';
import type { iCollectionResult, tListing, tSeed, tSynced } from './engine';
import type { tAnyCollection } from './types';

const FAST_PUSH_DELAY_MS = 800;
const RETRY_INTERVAL_MS = 15_000;

type tSyncStatus = 'idle' | 'syncing' | 'offline';

/**
 * - manual: the server is asked on start and when the connection returns, changes are only sent by save()
 * - auto: changes are kept on the device and sent as soon as the server can be reached, again whenever something
 *   changes. Offline (no internet or no backend) it keeps trying, and once connected there is nothing to do
 */
type tSyncMode = 'auto' | 'manual';

/**
 * Auto mode: when and how changes are sent
 * - pushDelay: how long nothing may change before they go out
 * - maxPushDelay: they go out after this long at the latest, however busy the user is
 * - listing: 'known' only writes the rows this device knows, 'server' asks the server first and also pulls what changed elsewhere
 * - refreshOnVisible: a full sync whenever the app comes back to the foreground
 */
interface iAutoOptions {
    pushDelay?: number;
    maxPushDelay?: number;
    listing?: tListing;
    refreshOnVisible?: boolean;
}

interface iSyncMeta {
    version: number;
    synced: Record<string, tSynced>;
    seed: Record<string, tSeed>;
}

interface iSyncReport {
    ok: boolean;
    busy?: boolean; // Another sync was already running, it will be run again afterwards if it was a save
    pushed: number;
    pulled: number;
    removed: number;
    overwritten: number;
    failed: number;
    error?: string;
}

interface iSyncInfo {
    recovered: boolean; // The sync worked after the app had been offline
}

type tResults = Record<string, iCollectionResult<object>>;

interface iTracked {
    collection: tAnyCollection;
    items: object[];
}

interface iUseSyncOptions<S> {
    mode: tSyncMode;
    /** Entries point to entries of the collections before them, this is also the order of saving */
    collections: tAnyCollection[];
    /** Bump when the row format changes: an older meta would make unchanged-looking entities count as deleted */
    version: number;
    /** The sync meta of the last session, as it was handed out by this hook */
    storedMeta?: unknown;
    /** Placeholders for a first run (the generated welcome content), they are replaced by the server's data */
    initialSeed?: () => Record<string, tSeed>;
    /** What the unsaved count and the automatic saving look at, nothing else counts as a change */
    tracked: iTracked[];
    /** Reads the items of every collection as they are right now, plus whatever apply needs to merge the result */
    read: () => { items: Record<string, object[]>; context: S };
    /** Merges the result into the app state, must keep everything that was changed after read() */
    apply: (results: tResults, context: S) => void;
    auto?: iAutoOptions;
    onSync?: (report: iSyncReport, info: iSyncInfo) => void;
}

const emptyMeta = (version: number, collections: tAnyCollection[]): iSyncMeta => ({
    version,
    synced: Object.fromEntries(collections.map(({ name }) => [name, {}])),
    seed: Object.fromEntries(collections.map(({ name }) => [name, {}])),
});

const isOnline = () => typeof navigator === 'undefined' || navigator.onLine;

const useSync = <S,>(options: iUseSyncOptions<S>) => {
    const { mode, collections, version, tracked } = options;
    const [meta, setMeta] = useState<iSyncMeta>(() => {
        const stored = options.storedMeta as iSyncMeta | undefined;
        if (stored?.version === version) {
            return stored;
        }
        const fresh = emptyMeta(version, collections);
        const seed = options.initialSeed?.();
        if (seed) {
            for (const { name } of collections) {
                fresh.seed[name] = seed[name] ?? {};
            }
        }
        return fresh;
    });
    const [status, setStatus] = useState<tSyncStatus>(() => (mode === 'auto' && !isOnline() ? 'offline' : 'idle'));

    const latest = useRef({ options, meta, status });
    latest.current = { options, meta, status };
    const running = useRef(false);
    const queued = useRef(false);
    // The changes the last failed attempt tried to send, they are not tried again until something changes
    const failedSignature = useRef<string | null>(null);
    // Since when changes are waiting, the delay of an automatic save is cut short by the maximum
    const waitingSince = useRef<number | null>(null);
    const { pushDelay = FAST_PUSH_DELAY_MS, maxPushDelay = Infinity, listing = 'known', refreshOnVisible = true } = options.auto ?? {};

    // Edits of children (blocks, sets) are expected to change their tracked parent as well, or be tracked themselves
    const dirty = useMemo(
        () =>
            Object.fromEntries(
                tracked.map(({ collection, items }) => [
                    collection.name,
                    findDirty(collection, items, meta.synced[collection.name] ?? {}, meta.seed[collection.name] ?? {}),
                ]),
            ),
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [meta, ...tracked.map(({ items }) => items)],
    );
    const unsavedCount = Object.values(dirty).reduce((sum, entry) => sum + entry.dirty.size + entry.deleted.length, 0);

    const signature = useMemo(() => {
        const parts: string[] = [];
        for (const { collection, items } of tracked) {
            const { dirty: keys, deleted } = dirty[collection.name];
            items.forEach((item) => keys.has(collection.key(item)) && parts.push(`${collection.name}:${collection.key(item)}:${hashOf(collection, item)}`));
            deleted.forEach((key) => parts.push(`${collection.name}:${key}:deleted`));
        }
        return parts.join('|');
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [dirty]);

    const sync = useCallback(async (push: boolean, listing: tListing = 'server'): Promise<iSyncReport> => {
        const report: iSyncReport = { ok: false, pushed: 0, pulled: 0, removed: 0, overwritten: 0, failed: 0 };
        if (running.current) {
            queued.current ||= push;
            return { ...report, busy: true };
        }
        running.current = true;
        const wasOffline = latest.current.status === 'offline';
        setStatus('syncing');

        const { options: current, meta: snapshotMeta } = latest.current;
        const { items, context } = current.read();
        // The collections that were synced, if a later one fails the writes of these must not be forgotten
        const finished: tResults = {};

        try {
            // What the collections saved so far ended up as, later ones look up the server ids of their relations here
            const done: Record<string, tSynced> = {};
            const results: tResults = {};
            for (const collection of current.collections) {
                const result = await syncCollection(
                    collection,
                    items[collection.name] ?? [],
                    snapshotMeta.synced[collection.name] ?? {},
                    snapshotMeta.seed[collection.name] ?? {},
                    push,
                    done,
                    listing,
                );
                done[collection.name] = result.synced;
                finished[collection.name] = result;
                results[collection.name] = result;
            }

            current.apply(results, context);

            const nextMeta = emptyMeta(current.version, current.collections);
            for (const { name } of current.collections) {
                nextMeta.synced[name] = results[name].synced;
                // A placeholder that is synced (or gone) is no placeholder anymore
                nextMeta.seed[name] = Object.fromEntries(
                    Object.entries(snapshotMeta.seed[name] ?? {}).filter(([key]) => !(key in results[name].synced)),
                );
                report.pushed += results[name].pushed;
                report.pulled += results[name].pulled;
                report.removed += results[name].removed;
                report.overwritten += results[name].overwritten;
                report.failed += results[name].failed;
            }
            setMeta(nextMeta);
            // A sync that was queued starts before the next render, it must not begin with the meta this one began with
            latest.current.meta = nextMeta;
            setStatus('idle');

            const succeeded = { ...report, ok: true };
            current.onSync?.(succeeded, { recovered: wasOffline });
            return succeeded;
        } catch (error) {
            // Rows that were created or deleted on the server stay known, or they would come back as strangers
            // and rows deleted here would not be deleted there
            const partial = emptyMeta(current.version, current.collections);
            partial.seed = snapshotMeta.seed;
            for (const { name } of current.collections) {
                const synced = { ...snapshotMeta.synced[name] };
                const result = finished[name];
                result?.pushedKeys.forEach((key) => (synced[key] = result.synced[key]));
                result?.removedKeys.forEach((key) => delete synced[key]);
                partial.synced[name] = synced;
            }
            setMeta(partial);
            latest.current.meta = partial;
            setStatus('offline');
            const failed = { ...report, error: error instanceof Error ? error.message : String(error) };
            current.onSync?.(failed, { recovered: false });
            return failed;
        } finally {
            running.current = false;
            if (queued.current) {
                queued.current = false;
                void sync(true);
            }
        }
    }, []);

    // On start and when the connection returns. Manual only pulls, nothing is sent without save()
    useEffect(() => {
        const full = () => void sync(mode === 'auto');
        if (mode === 'manual' || isOnline()) {
            full();
        }
        const goOffline = () => mode === 'auto' && setStatus('offline');
        const onVisible = () => {
            if (mode !== 'auto') {
                return;
            }
            if (document.visibilityState === 'visible') {
                if (refreshOnVisible) full();
            } else if (waitingSince.current !== null && isOnline()) {
                // Timers of a page in the background are paused or killed, send what is waiting before it goes
                waitingSince.current = null;
                void sync(true, listing);
            }
        };
        window.addEventListener('online', full);
        window.addEventListener('offline', goOffline);
        document.addEventListener('visibilitychange', onVisible);
        return () => {
            window.removeEventListener('online', full);
            window.removeEventListener('offline', goOffline);
            document.removeEventListener('visibilitychange', onVisible);
        };
    }, [mode, sync, listing, refreshOnVisible]);

    // Auto: changes go out shortly after they were made, without asking the server first
    useEffect(() => {
        if (!signature) {
            waitingSince.current = null;
        }
        if (mode !== 'auto' || !signature || status !== 'idle' || signature === failedSignature.current) {
            return;
        }
        waitingSince.current ??= Date.now();
        const delay = Math.min(pushDelay, Math.max(0, waitingSince.current + maxPushDelay - Date.now()));
        const timer = setTimeout(async () => {
            waitingSince.current = null;
            const report = await sync(true, listing);
            if (report.busy) {
                return;
            }
            failedSignature.current = report.ok && report.failed === 0 ? null : signature;
            // Rows that were changed or deleted elsewhere are settled by asking the server
            if (report.ok && report.failed > 0 && listing === 'known') {
                void sync(true);
            }
        }, delay);
        return () => clearTimeout(timer);
    }, [mode, signature, status, sync, pushDelay, maxPushDelay, listing]);

    // Auto: no internet or no backend, look again from time to time
    useEffect(() => {
        if (mode !== 'auto' || status !== 'offline') {
            return;
        }
        const timer = setInterval(() => isOnline() && void sync(true), RETRY_INTERVAL_MS);
        return () => clearInterval(timer);
    }, [mode, status, sync]);

    const save = useCallback(() => sync(true), [sync]);

    return { dirty, meta, save, status, unsavedCount };
};

export type { iAutoOptions, iSyncInfo, iSyncMeta, iSyncReport, iTracked, iUseSyncOptions, tSyncMode, tSyncStatus };

export default useSync;