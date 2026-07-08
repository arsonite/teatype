/**
 * @license
 * Copyright (C) 2024-2026 Burak Günaydin
 *
 * Permission is hereby granted, free of charge, to unknown person obtaining a copy
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
import { SetStateAction, useState } from 'react';
import { Toaster } from 'react-hot-toast';

// Components
import { DynamicResourceView } from './DynamicResourceView';
import { TeaConfirmProvider, TeaPanel } from '@teatype/components';

// Hooks
import { useAPIRegistry } from '@teatype/hooks';

/** Fields to hide from the table per resource, on top of computed fields (e.g. noisy/internal attributes) */
const ATTRIBUTE_BLACKLIST: Record<string, string[]> = {};

/**
 * A dynamic dashboard that auto-generates views for all resources
 * registered in the HSDB API Registry.
 *
 * @example
 * ```tsx
 * // Renders a complete admin dashboard for all registered models
 * <DynamicDashboard />
 * ```
 */
export function DynamicDashboard() {
    const { loading, error, apiInfos, refresh } = useAPIRegistry();
    const [selectedResource, setSelectedResource] = useState<string | null>(null);

    if (error) {
        return (
            <div className='hsdb-dashboard hsdb-dashboard--error'>
                <div className='error'>
                    Failed to load API Registry: {error}
                    <button onClick={refresh}>Retry</button>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className='hsdb-dashboard hsdb-dashboard--loading'>
                <div className='loading'>Loading API Registry...</div>
            </div>
        );
    }

    // If no resource is selected, show the overview
    if (!selectedResource) {
        return (
            <TeaConfirmProvider>
                <div className='hsdb-dashboard'>
                    <div className='hsdb-dashboard__stats'>
                        {apiInfos.map(
                            (info: {
                                endpoint: string;
                                allowedMethods: { resource: unknown[]; collection: unknown[] };
                                name: unknown;
                                resource: SetStateAction<string | null>;
                                count: unknown;
                            }) => (
                                <TeaPanel
                                    tags={info.allowedMethods.resource
                                        .map((m: unknown) => ({
                                            color: '#e3f2fd',
                                            name: m,
                                            textColor: '#1565c0',
                                        }))
                                        .concat(
                                            info.allowedMethods.collection.map((m: unknown) => ({
                                                color: '#fce4ec',
                                                name: m,
                                                textColor: '#c62828',
                                            })),
                                        )}
                                    title={info.endpoint.replace('\/', '')}
                                    variant='stat'
                                    onClick={() => setSelectedResource(info.resource)}
                                >
                                    {info.count}
                                </TeaPanel>
                            ),
                        )}
                    </div>
                </div>
            </TeaConfirmProvider>
        );
    }

    // Show the selected resource view
    return (
        <TeaConfirmProvider>
            <div className='hsdb-dashboard'>
                <Toaster position='top-right' />

                <div className='hsdb-dashboard__breadcrumb'>
                    <button className='btn btn--secondary' onClick={() => setSelectedResource(null)}>
                        ← Back to Dashboard
                    </button>
                </div>

                <DynamicResourceView
                    resource={selectedResource}
                    attributeBlacklist={ATTRIBUTE_BLACKLIST[selectedResource]}
                />
            </div>
        </TeaConfirmProvider>
    );
}

export default DynamicDashboard;
