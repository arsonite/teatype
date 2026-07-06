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
import { ReactElement } from 'react';

// Types
import type { tTeaTag } from '@teatype/types';

// Style
import './style/TeaPanel.scss';

interface iTeaPanelProps {
    borderThickness?: 'thin' | 'medium' | 'thick';
    children: React.ReactNode;
    className?: string;
    id?: string;
    padding?: 'none' | 'small' | 'medium' | 'large';
    size?: 'dymnamic' | 'full';
    tags?: tTeaTag[];
    title?: string;
    useTheme?: boolean;
    variant?: 'card' | 'framed' | 'stat';

    onClick?: () => void;
}

const TeaPanel: React.FC<iTeaPanelProps> = (props) => {
    const classes = [
        'tea-panel',
        props.className || '',
        props.padding ? `padding-${props.padding}` : 'padding-none',
        props.size ? `size-${props.size}` : 'size-dynamic',
        props.useTheme && 'use-theme',
        props.variant ? `variant-${props.variant}` : 'variant-default',
        props.onClick && 'clickable',
    ]
        .filter(Boolean)
        .join(' ');

    const wrapComponent = (content: ReactElement) => {
        if (props.variant === 'framed') {
            return <fieldset>{content}</fieldset>;
        }
        return content;
    };

    return (
        <div className={classes}>
            {wrapComponent(
                <>
                    {props.title && <legend className='title'>{props.title}</legend>}

                    <div className='children'>{props.children}</div>

                    {props.tags && (
                        <div className='tags'>
                            {props.tags.map((tag, index) => {
                                const darkenColor = (color: string): string => {
                                    if (color.startsWith('var(')) {
                                        return color.replace(')', '-dark)');
                                    }
                                    // Darken hex color by 50%
                                    const hex = color.replace('#', '');
                                    const num = parseInt(hex, 16);
                                    const darkNum = Math.floor(num * 0.5);
                                    return '#' + darkNum.toString(16).padStart(6, '0');
                                };

                                const lightenColor = (color: string): string => {
                                    if (color.startsWith('var(')) {
                                        return color.replace(')', '-light)');
                                    }
                                    // Lighten hex color by 50%
                                    const hex = color.replace('#', '');
                                    const num = parseInt(hex, 16);
                                    const lightNum = Math.floor(num + (0xffffff - num) * 0.5);
                                    return '#' + lightNum.toString(16).padStart(6, '0');
                                };

                                const bgColor = tag.color || lightenColor('var(--accent)');
                                const textColor = darkenColor(bgColor);

                                return (
                                    <span
                                        key={index}
                                        className='tag'
                                        style={{
                                            backgroundColor: bgColor,
                                            color: textColor,
                                        }}
                                    >
                                        {tag.name}
                                    </span>
                                );
                            })}
                        </div>
                    )}
                </>,
            )}
        </div>
    );
};

export default TeaPanel;

export { TeaPanel };
