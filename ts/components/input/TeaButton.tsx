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
import React, { useMemo, useRef, useCallback } from 'react';

// Components
import { TeaIcon } from '../TeaIcon';

// Style
import './style/TeaButton.scss';

type tButtonAlign = 'center' | 'start';
type tButtonSize = 'xs' | 'small' | 'medium' | 'large';
type tButtonTheme = 'default' | 'filled' | 'success' | 'danger' | 'ghost';
type tButtonVariant = 'default' | 'borderless';

/**
 * The one button of the apps. Everything that is clicked is this component, the look comes from its props:
 *
 * - `theme` is the color: default, filled (the main action), danger, success, ghost
 * - `variant` is the surface: default (with border) or borderless (only visible on hover)
 * - `size` is xs, small, medium or large; a button without text (only `icon`, an icon as child, or nothing at all like a
 *   color swatch) is a square of that size
 * - `active` marks a selected one (toggle, tab, chosen option), `round` makes it a circle, `fullWidth` + `align='start'`
 *   makes a row of a list or menu
 * - `--tea-button-size` overrides the side of a square button for one place
 */
interface iTeaButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    active?: boolean;
    align?: tButtonAlign;
    children?: React.ReactNode;
    className?: string;
    /** Disable ripple effect (default: false) */
    disableRipple?: boolean;
    fullWidth?: boolean;
    icon?: React.ReactNode;
    /** Force the square shape for a glyph that is not an icon component, like a letter (default: detected from the children) */
    iconOnly?: boolean;
    iconPosition?: 'left' | 'right';
    id?: string;
    loading?: boolean;
    /** Turn the icon by 45 degrees while hovered, for the plus that becomes a cross (default: false) */
    rotateIcon?: boolean;
    round?: boolean;
    size?: tButtonSize;
    theme?: tButtonTheme;
    variant?: tButtonVariant;
}

const hasContent = (children: React.ReactNode) =>
    React.Children.toArray(children).some((child) => (typeof child === 'string' ? child.trim().length > 0 : !!child));

const TeaButton = React.forwardRef<HTMLButtonElement, iTeaButtonProps>(function TeaButton(props, forwardedRef) {
    const {
        active,
        align = 'center',
        children,
        className,
        disableRipple = false,
        disabled,
        fullWidth = false,
        icon,
        iconOnly: iconOnlyProp,
        iconPosition = 'left',
        loading = false,
        onClick,
        rotateIcon = false,
        round = false,
        size = 'medium',
        theme = 'default',
        type = 'button',
        variant = 'default',
        ...rest
    } = props;

    const buttonRef = useRef<HTMLButtonElement | null>(null);
    const setRef = useCallback(
        (node: HTMLButtonElement | null) => {
            buttonRef.current = node;
            if (typeof forwardedRef === 'function') forwardedRef(node);
            else if (forwardedRef) forwardedRef.current = node;
        },
        [forwardedRef],
    );

    /** Spawn a Material-UI style ripple circle at the click coordinates */
    const spawnRipple = useCallback(
        (e: React.MouseEvent<HTMLButtonElement>) => {
            if (disableRipple || disabled || loading) return;

            const button = buttonRef.current;
            if (!button) return;

            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Diameter must cover the furthest corner
            const diameter =
                Math.max(
                    Math.hypot(x, y),
                    Math.hypot(rect.width - x, y),
                    Math.hypot(x, rect.height - y),
                    Math.hypot(rect.width - x, rect.height - y),
                ) * 2;

            const ripple = document.createElement('span');
            ripple.className = 'tea-button__ripple';
            ripple.style.width = `${diameter}px`;
            ripple.style.height = `${diameter}px`;
            ripple.style.left = `${x - diameter / 2}px`;
            ripple.style.top = `${y - diameter / 2}px`;

            button.appendChild(ripple);

            // Clean up after animation finishes
            ripple.addEventListener('animationend', () => {
                ripple.remove();
            });
        },
        [disableRipple, disabled, loading],
    );

    const handleClick = useCallback(
        (e: React.MouseEvent<HTMLButtonElement>) => {
            spawnRipple(e);
            onClick?.(e);
        },
        [spawnRipple, onClick],
    );

    // No text: only an icon, a single icon as child, or nothing at all (a color swatch)
    const detectedIconOnly = useMemo(() => {
        const content = React.Children.toArray(children).filter((child) =>
            typeof child === 'string' ? child.trim().length > 0 : !!child,
        );
        if (content.length === 0) return true;
        if (content.length !== 1 || icon) return false;
        const child = content[0];
        return (
            React.isValidElement(child) &&
            (child.type === 'svg' ||
                child.type === TeaIcon ||
                (typeof child.type === 'function' && (child.type as Function).name?.endsWith('Icon')))
        );
    }, [children, icon]);
    const iconOnly = iconOnlyProp ?? detectedIconOnly;

    const classes = [
        'tea-button',
        !disableRipple && 'ripple',
        rotateIcon && 'icon-rotation',
        iconOnly ? `size-icon-only size-${size}` : `size-${size}`,
        `theme-${theme}`,
        `variant-${variant}`,
        align === 'start' && 'align-start',
        active && 'active',
        fullWidth && 'full-width',
        round && 'round',
        loading && 'loading',
        className,
    ]
        .filter(Boolean)
        .join(' ');

    return (
        <button
            ref={setRef}
            className={classes}
            type={type}
            aria-pressed={active}
            disabled={disabled || loading}
            {...rest}
            onClick={handleClick}
        >
            {loading && (
                <span className='spinner'>
                    <svg viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2'>
                        <circle cx='12' cy='12' r='10' opacity='0.25' />
                        <path d='M12 2a10 10 0 0 1 10 10' />
                    </svg>
                </span>
            )}

            {icon && iconPosition === 'left' && !loading && <span className='icon'>{icon}</span>}

            {hasContent(children) ? children : null}

            {icon && iconPosition === 'right' && !loading && <span className='icon'>{icon}</span>}
        </button>
    );
});

export type { iTeaButtonProps, tButtonAlign, tButtonSize, tButtonTheme, tButtonVariant };

export default TeaButton;

export { TeaButton };
