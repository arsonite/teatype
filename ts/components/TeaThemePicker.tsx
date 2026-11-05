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

// Utility
import { getThemes, type iTeaTheme } from '@teatype/toolkit/themes';

// Style
import './style/TeaThemePicker.scss';

interface iTeaThemePickerProps {
    onChange: (theme: string) => void;
    themes?: iTeaTheme[]; // All registered themes if not given
    value: string;
}

// The themes as cards, each card shows the colors of its own theme
export const TeaThemePicker: React.FC<iTeaThemePickerProps> = ({ value, onChange, themes = getThemes() }) => (
    <div className='tea-theme-picker'>
        {themes.map((theme) => (
            <button
                key={theme.id}
                className={`tea-theme-option ${value === theme.id ? 'tea-theme-option--active' : ''}`}
                onClick={() => onChange(theme.id)}
            >
                <span className='tea-theme-preview' data-theme={theme.id} />
                <span className='tea-theme-option__label'>{theme.label}</span>
                <span className='tea-theme-option__description'>{theme.description}</span>
            </button>
        ))}
    </div>
);

export default TeaThemePicker;
