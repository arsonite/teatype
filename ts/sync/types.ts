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

// API
import type { HSDBBaseAPI, HSDBEntity } from '../api';

type tRow = Record<string, string | number | boolean>;

// What the server delivers: its entry id, the `rev` of the last write by a client (the model needs a required int
// attribute of that name) and the fields of the model
type tServerRow = HSDBEntity & { rev: number } & Record<string, unknown>;

/**
 * Maps one local entity type to one HSDB model. The key identifies the entity in the browser only: the server
 * hands out its own entry ids, the sync keeps track of which key belongs to which id (see engine.ts).
 *
 * toRow() must produce the same key order every time: its JSON decides whether an entity changed since the last
 * sync, so it contains neither the id nor the rev. Relation fields hold the key of the related entity (the sync
 * swaps keys and server ids at the boundary) and are left out when the relation is not set.
 */
interface iCollection<L extends object> {
    api: typeof HSDBBaseAPI;
    name: string;
    relations?: Record<string, string>; // Relation field -> name of the collection it points to
    listFields?: string[];

    fromRow: (row: tServerRow, key: string) => L;
    key: (item: L) => string;
    // For models where the content decides which row is which (the single settings row, presets by position):
    // a server row without a known key is matched to the local entity with this key. Needs the fields it reads.
    slot?: (row: tServerRow) => string;
    toRow: (item: L) => tRow;
}

// A collection of any item type, for lists that mix them
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type tAnyCollection = iCollection<any>;

export type { iCollection, tAnyCollection, tRow, tServerRow };
