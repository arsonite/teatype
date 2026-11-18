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
import React from 'react';

// Style
import './style/TeaSyncStatus.scss';

interface iTeaSyncStatusProps {
    /** auto: changes are sent by themselves, manual: they wait for onSave. Default: auto */
    mode?: 'auto' | 'manual';
    status: 'idle' | 'offline' | 'syncing';
    /** Changes the server does not have yet */
    unsavedCount: number;
    onSave?: () => void;
}

const plural = (count: number) => `${count} change${count === 1 ? '' : 's'}`;

/**
 * The state of the sync (see @teatype/sync) in one line, for the footer of a sidebar. In manual mode the line
 * is a button that saves.
 */
const TeaSyncStatus: React.FC<iTeaSyncStatusProps> = ({ mode = 'auto', status, unsavedCount, onSave }) => {
    const waiting = status === 'idle' && unsavedCount > 0;
    const label =
        status === 'syncing'
            ? 'Syncing…'
            : status === 'offline'
              ? unsavedCount > 0
                  ? `Offline, ${plural(unsavedCount)} kept on this device`
                  : 'Offline'
              : unsavedCount > 0
                ? mode === 'manual'
                    ? `${plural(unsavedCount)} not saved`
                    : `${plural(unsavedCount)} to sync`
                : 'Synced';
    const className = `tea-sync-status tea-sync-status--${waiting ? 'waiting' : status}`;

    if (mode === 'manual' && onSave) {
        return (
            <button className={className} title='Save to the server' onClick={onSave}>
                <span className='tea-sync-status__dot' />
                {label}
            </button>
        );
    }
    return (
        <div className={className} role='status'>
            <span className='tea-sync-status__dot' />
            {label}
        </div>
    );
};

export { TeaSyncStatus };

export type { iTeaSyncStatusProps };
