/**
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

// Icons
import { CheckIcon } from '../../icons';

// Style
import './style/TeaCheckbox.scss';

interface iTeaCheckboxProps {
    checked: boolean;
    className?: string;
    disabled?: boolean;
    label?: React.ReactNode;
    onChange: (checked: boolean) => void;
}

// A checkbox that is drawn by teatype instead of the browser, the native input stays for the keyboard and screen readers
export const TeaCheckbox: React.FC<iTeaCheckboxProps> = ({ checked, onChange, label, disabled, className = '' }) => (
    <label
        className={`tea-checkbox ${checked ? 'tea-checkbox--checked' : ''} ${
            disabled ? 'tea-checkbox--disabled' : ''
        } ${className}`}
    >
        <input
            className='tea-checkbox__input'
            type='checkbox'
            checked={checked}
            disabled={disabled}
            onChange={(event) => onChange(event.target.checked)}
        />
        <span className='tea-checkbox__box'>{checked && <CheckIcon />}</span>
        {label && <span className='tea-checkbox__label'>{label}</span>}
    </label>
);

export default TeaCheckbox;
