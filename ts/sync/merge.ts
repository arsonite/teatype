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

/**
 * Takes the sync result for the entities that were not touched while the request was in flight, keeps everything
 * the user changed or created in the meantime, and adds entities that are new from the server.
 * Items are replaced when they change, never mutated, so an untouched item is the same object as in the snapshot.
 *
 * @param key Identity of an item
 * @param current The items now
 * @param snapshot The items the sync started with
 * @param result The items the sync ended with
 */
const mergeItems = <L extends object>(key: (item: L) => string, current: L[], snapshot: L[], result: L[]): L[] => {
    const snapshotByKey = new Map(snapshot.map((item) => [key(item), item]));
    const resultByKey = new Map(result.map((item) => [key(item), item]));
    const seen = new Set<string>();
    const merged: L[] = [];

    for (const item of current) {
        const id = key(item);
        seen.add(id);
        if (snapshotByKey.get(id) !== item) {
            merged.push(item);
            continue;
        }
        const synced = resultByKey.get(id);
        if (synced) {
            merged.push(synced);
        }
    }
    for (const item of result) {
        const id = key(item);
        if (!seen.has(id) && !snapshotByKey.has(id)) {
            merged.push(item);
        }
    }
    return merged;
};

export { mergeItems };
