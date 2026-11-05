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

// The themes of all apps. dark, flow and light come with teatype (style/globthemes.scss), an app adds its own with
// the tea-theme mixin of style/globvars.scss and registers them here: registerThemes([{ id: 'ocean', ... }]).
interface iTeaTheme {
    description: string;
    id: string;
    label: string;
    light: boolean; // Light themes get the light-mode class on the body, for dark-text overrides of apps
}

const DEFAULT_THEMES: readonly iTeaTheme[] = [
    { id: 'dark', label: 'Dark', description: 'Black and gray with orange accents', light: false },
    { id: 'flow', label: 'Flow', description: 'Deep blue with purple accents', light: false },
    { id: 'light', label: 'Light', description: 'Clean white with indigo accents', light: true },
];

let appThemes: iTeaTheme[] = [];

// The themes of an app, they are listed before the default ones. A theme with a known id replaces that one.
const registerThemes = (themes: iTeaTheme[]): void => {
    appThemes = [...themes, ...appThemes.filter((known) => !themes.some((theme) => theme.id === known.id))];
};

const getThemes = (): iTeaTheme[] => [
    ...appThemes,
    ...DEFAULT_THEMES.filter((theme) => !appThemes.some((known) => known.id === theme.id)),
];

const isLightTheme = (id: string): boolean => getThemes().find((theme) => theme.id === id)?.light ?? false;

// The id if it is a known theme, the fallback otherwise
const themeOf = (id: unknown, fallback: string): string => (getThemes().some((theme) => theme.id === id) ? (id as string) : fallback);

// Puts the theme on the page, the toast and the modals live in the body and get it from there
const applyTheme = (id: string): void => {
    document.documentElement.dataset.theme = id;
    document.body.classList.toggle('light-mode', isLightTheme(id));
};

export { DEFAULT_THEMES, applyTheme, getThemes, isLightTheme, registerThemes, themeOf };

export type { iTeaTheme };
