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

/// <reference types="vite/client" />

// React imports
import React from 'react';

// Icons
import { ArrowIcon } from '../icons';

interface iTeaHubLinkProps {
    /** Where the hub lives, a full page load because the hub is an app of its own. Default: / */
    href?: string;
    label?: string;
    /** row: full-width line of the sidebar, rail: icon button of the collapsed sidebar */
    variant?: 'row' | 'rail';
}

// Served on /, an app runs standalone. Published under a path (homepie: /<name>/), the hub is the page at /.
const isEmbedded = (): boolean => import.meta.env.BASE_URL !== '/';

/**
 * Link back to the hub (homepie) an app is embedded in. Renders nothing when the app runs standalone.
 */
const TeaHubLink: React.FC<iTeaHubLinkProps> = ({ href = '/', label = 'Back to hub', variant = 'row' }) => {
    if (!isEmbedded()) {
        return null;
    }

    return variant === 'rail' ? (
        <a className='tea-rail__btn tea-hub-link tea-hub-link--rail' href={href} title={label}>
            <ArrowIcon />
        </a>
    ) : (
        <a className='tea-hub-link' href={href}>
            <span className='tea-hub-link__icon'>
                <ArrowIcon />
            </span>
            {label}
        </a>
    );
};

export type { iTeaHubLinkProps };
export { TeaHubLink, isEmbedded };
export default TeaHubLink;
