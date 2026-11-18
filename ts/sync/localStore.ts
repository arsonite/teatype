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

// The local copy of an app's data lives in IndexedDB, localStorage ends at about 5 MB. Values are stored as they
// are, not as JSON text. One database per app with a single key-value object store.

interface iLocalStore {
    /** Reads one value, undefined if nothing is stored */
    read: <T>(key: string) => Promise<T | undefined>;
    /** Reads several values, never rejects: if IndexedDB fails (private mode) the app starts empty */
    readAll: (keys: string[]) => Promise<Record<string, unknown>>;
    /** Writes values in ONE transaction, so data and the sync meta of the same moment are never split */
    write: (values: Record<string, unknown>) => Promise<void>;
}

const createLocalStore = (name: string): iLocalStore => {
    const STORE = 'kv';
    let opened: Promise<IDBDatabase> | null = null;

    const open = (): Promise<IDBDatabase> => {
        opened ??= new Promise((resolve, reject) => {
            const request = indexedDB.open(name, 1);
            request.onupgradeneeded = () => request.result.createObjectStore(STORE);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
        return opened;
    };

    // Resolves when the transaction completed, so a resolved write is really committed
    const run = async <T>(mode: IDBTransactionMode, work: (store: IDBObjectStore) => IDBRequest<T>[]): Promise<T[]> => {
        const db = await open();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(STORE, mode);
            const requests = work(transaction.objectStore(STORE));
            transaction.oncomplete = () => resolve(requests.map((request) => request.result));
            transaction.onerror = () => reject(transaction.error);
            transaction.onabort = () => reject(transaction.error);
        });
    };

    return {
        read: async <T>(key: string) => (await run('readonly', (store) => [store.get(key) as IDBRequest<T>]))[0],
        readAll: async (keys) => {
            try {
                const values = await run('readonly', (store) => keys.map((key) => store.get(key)));
                return Object.fromEntries(keys.map((key, index) => [key, values[index]]));
            } catch (error) {
                console.error('IndexedDB is not available, nothing is saved in this browser', error);
                return {};
            }
        },
        write: async (values) => {
            await run('readwrite', (store) => Object.entries(values).map(([key, value]) => store.put(value, key)));
        },
    };
};

export type { iLocalStore };
export { createLocalStore };
