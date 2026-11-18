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
import React, { useEffect, useId, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

// Style
import './style/TeaAutocomplete.scss';

interface iTeaAutocompleteOption {
    label: string;
    value: string | number;
}

interface iTeaAutocompleteProps {
    className?: string;
    disabled?: boolean;
    error?: string;
    hint?: string;
    label?: string;
    noOptionsText?: string;
    options: iTeaAutocompleteOption[];
    placeholder?: string;
    value: string | number | null | undefined;

    onChange: (value: string) => void;
}

const MAX_HEIGHT = 280;
const MARGIN = 8;

/** Ignores case and accents, so "cafe" finds "Café" */
const normalize = (text: string): string => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

/**
 * Like the MUI Autocomplete, but only for choosing one of the options: the typed text filters the list, it never becomes a value.
 * The list lives in the body and scrolls by itself, so a modal or a container that clips does not cut it off.
 */
export const TeaAutocomplete: React.FC<iTeaAutocompleteProps> = ({
    className = '',
    disabled,
    error,
    hint,
    label,
    noOptionsText = 'No match',
    options,
    placeholder,
    value,

    onChange,
}) => {
    const id = useId();
    const input = useRef<HTMLInputElement>(null);
    const list = useRef<HTMLUListElement>(null);

    const [open, setOpen] = useState(false);
    // null: show the chosen option, a string: what is being typed
    const [query, setQuery] = useState<string | null>(null);
    const [active, setActive] = useState(0);
    const [box, setBox] = useState<{ left: number; width: number; top?: number; bottom?: number; maxHeight: number }>({ left: 0, width: 0, maxHeight: MAX_HEIGHT });

    const selected = options.find((option) => String(option.value) === String(value));
    const shown = open && query !== null ? query : (selected?.label ?? '');

    const filtered = useMemo(() => {
        const needle = normalize((query ?? '').trim());
        return needle ? options.filter((option) => normalize(option.label).includes(needle)) : options;
    }, [options, query]);

    const close = () => {
        setOpen(false);
        setQuery(null);
    };

    const choose = (option: iTeaAutocompleteOption | undefined) => {
        if (option) {
            onChange(String(option.value));
        }
        close();
        input.current?.blur();
    };

    const openList = () => {
        if (!open) {
            setOpen(true);
            setQuery(null);
            setActive(Math.max(0, options.findIndex((option) => String(option.value) === String(value))));
        }
    };

    // Below the field, or above it when there is more room there
    const place = () => {
        const rect = input.current?.getBoundingClientRect();
        if (!rect) {
            return;
        }
        const below = window.innerHeight - rect.bottom - MARGIN;
        const above = rect.top - MARGIN;
        const up = below < 160 && above > below;
        setBox({
            left: rect.left,
            width: rect.width,
            maxHeight: Math.min(MAX_HEIGHT, up ? above : below),
            ...(up ? { bottom: window.innerHeight - rect.top + 4 } : { top: rect.bottom + 4 }),
        });
    };

    useLayoutEffect(() => {
        if (!open) {
            return;
        }
        place();
        const onScroll = (event: Event) => !list.current?.contains(event.target as Node) && place();
        window.addEventListener('resize', place);
        document.addEventListener('scroll', onScroll, true);
        return () => {
            window.removeEventListener('resize', place);
            document.removeEventListener('scroll', onScroll, true);
        };
    }, [open]);

    // The highlighted option stays visible (also right after opening, when the list got its height)
    useEffect(() => {
        const scroller = list.current;
        const item = scroller?.querySelector<HTMLElement>(`[data-index='${active}']`);
        if (!open || !scroller || !item) {
            return;
        }
        const bottom = item.offsetTop + item.offsetHeight;
        if (item.offsetTop < scroller.scrollTop) {
            scroller.scrollTop = item.offsetTop - 4;
        } else if (bottom > scroller.scrollTop + scroller.clientHeight) {
            scroller.scrollTop = bottom - scroller.clientHeight + 4;
        }
    }, [open, active, filtered, box.maxHeight]);

    const onKeyDown = (event: React.KeyboardEvent) => {
        if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
            event.preventDefault();
            if (!open) {
                openList();
                return;
            }
            const step = event.key === 'ArrowDown' ? 1 : -1;
            setActive((current) => (filtered.length ? (current + step + filtered.length) % filtered.length : 0));
        } else if (event.key === 'Enter' && open) {
            event.preventDefault();
            choose(filtered[active]);
        } else if (event.key === 'Escape' && open) {
            event.stopPropagation();
            close();
        }
    };

    const listbox = `${id}-list`;

    return (
        <div className={`tea-input-group tea-autocomplete ${error ? 'tea-input-group--error' : ''} ${className}`}>
            {label && (
                <label htmlFor={id} className='tea-input-group__label'>
                    {label}
                </label>
            )}
            <input
                id={id}
                ref={input}
                className='tea-input-group__input tea-autocomplete__input'
                role='combobox'
                aria-autocomplete='list'
                aria-controls={listbox}
                aria-expanded={open}
                aria-activedescendant={open && filtered[active] ? `${id}-${active}` : undefined}
                autoComplete='off'
                disabled={disabled}
                placeholder={placeholder}
                value={shown}
                onBlur={close}
                onChange={(event) => {
                    setOpen(true);
                    setQuery(event.target.value);
                    setActive(0);
                }}
                onClick={openList}
                onFocus={(event) => {
                    openList();
                    event.target.select();
                }}
                onKeyDown={onKeyDown}
            />
            {error && <span className='tea-input-group__error'>{error}</span>}
            {hint && !error && <span className='tea-input-group__hint'>{hint}</span>}
            {open &&
                createPortal(
                    <ul
                        id={listbox}
                        ref={list}
                        className='tea-autocomplete__list'
                        role='listbox'
                        style={box}
                        // Keeps the focus in the field, so the list does not close before the click arrives
                        onMouseDown={(event) => event.preventDefault()}
                    >
                        {filtered.map((option, index) => (
                            <li
                                key={option.value}
                                id={`${id}-${index}`}
                                data-index={index}
                                className={`tea-autocomplete__option ${index === active ? 'tea-autocomplete__option--active' : ''} ${
                                    option === selected ? 'tea-autocomplete__option--selected' : ''
                                }`}
                                role='option'
                                aria-selected={option === selected}
                                onClick={() => choose(option)}
                                onMouseMove={() => active !== index && setActive(index)}
                            >
                                {option.label}
                            </li>
                        ))}
                        {!filtered.length && <li className='tea-autocomplete__empty'>{noOptionsText}</li>}
                    </ul>,
                    document.body,
                )}
        </div>
    );
};

export type { iTeaAutocompleteOption, iTeaAutocompleteProps };

export default TeaAutocomplete;
