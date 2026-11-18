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

/*
 * Local-first sync of IndexedDB collections with an HSDB backend.
 * useSync({ mode: 'manual' }): pulls on open and reconnect, pushes only when save() is called (lockkliye).
 * useSync({ mode: 'auto' }): works offline, pushes every change by itself and syncs on reconnect (tickfit).
 * Pair it with createLocalStore + usePersist for the device copy, mergeItems for applying results, TeaSyncStatus for the UI.
 */

export { findDirty, hashOf, syncCollection } from './engine';
export type { iCollectionResult, tListing, tSeed, tSynced } from './engine';
export { createLocalStore } from './localStore';
export type { iLocalStore } from './localStore';
export { mergeItems } from './merge';
export type { iCollection, tAnyCollection, tRow, tServerRow } from './types';
export { default as useSync } from './useSync';
export type { iSyncInfo, iSyncMeta, iSyncReport, iTracked, iUseSyncOptions, tSyncMode, tSyncStatus } from './useSync';
export { usePersist } from './usePersist';
