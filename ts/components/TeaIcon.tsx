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
import { type CSSProperties, memo, useMemo } from 'react';
import SVG, { type ErrorCallback, type LoadCallback } from 'react-inlinesvg';

// Utility
import { path } from '@teatype/toolkit/path';

import './style/TeaIcon.scss';

interface iTeaIconProps {
    readonly animated?: boolean;
    readonly children?: React.ReactNode;
    readonly className?: string;
    readonly color?: string;
    readonly filled?: boolean;
    readonly id?: string;
    readonly height?: string | number;
    readonly path?: readonly string[];
    readonly style?: CSSProperties;
    readonly theme?: 'text-primary' | 'text-secondary' | 'accent';
    readonly width?: string | number;

    readonly onClick?: React.MouseEventHandler<HTMLElement>;
    readonly onError?: ErrorCallback;
    readonly onLoad?: LoadCallback;
    readonly onMouseDown?: React.MouseEventHandler<HTMLElement>;
    readonly onTouchStart?: React.TouchEventHandler<HTMLElement>;
}

const resolveIconSource = (segments: readonly string[], isFilled: boolean, isAnimated: boolean): string => {
    const resolved = [...segments];

    if (isFilled && resolved.length > 0) {
        const lastIndex = resolved.length - 1;
        resolved[lastIndex] = `${resolved[lastIndex]}-filled`;
    }

    return isAnimated ? path.anim(...resolved) : path.icon(...resolved);
};

/**
 * SVG icon renderer. If an icon is missing, it's missing — no fallback.
 * Pass either a `path` to load via react-inlinesvg, or an inline `<svg>` as children.
 */
const TeaIcon = memo<iTeaIconProps>(function TeaIcon({
    animated = false,
    children,
    className,
    color = null,
    filled = false,
    height = '100%',
    id,
    path,
    style,
    theme = 'text-primary',
    width = 'auto',
    onClick,
    onError,
    onLoad,
    onMouseDown,
    onTouchStart,
}) {
    const svgSource = useMemo(
        () => (path ? resolveIconSource(path, filled, animated) : undefined),
        [path, filled, animated],
    );

    const containerClasses = useMemo(() => ['tea-icon', className].filter(Boolean).join(' '), [className]);

    if (color === null) {
        color = `var(--${theme})`;
    }
    style = useMemo(
        () => ({
            ...style,
            height,
            width,
            svg: {
                color: color,
                fill: color,
                stroke: color,
            },
        }),
        [style, height, color, width],
    );

    return (
        <picture
            id={id}
            className={containerClasses}
            style={style}
            onClick={onClick}
            onMouseDown={onMouseDown}
            onTouchStart={onTouchStart}
        >
            {svgSource ? <SVG cacheRequests src={svgSource} onError={onError} onLoad={onLoad} /> : children}
        </picture>
    );
});

export default TeaIcon;

export { TeaIcon };

export type { iTeaIconProps };
