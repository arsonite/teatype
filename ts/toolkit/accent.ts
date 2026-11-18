/**
 * @license
 * Copyright (C) 2024-2026 Burak Günaydin
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

const HEX = /^#[0-9a-f]{6}$/i;

/** A stored accent color that is not a #rrggbb falls back to the default of the app */
const sanitizeAccent = (value: unknown, fallback: string): string => (typeof value === 'string' && HEX.test(value) ? value : fallback);

/** The accent variables of a color: hover is lighter on a dark and darker on a light background, the glow is a veil */
const accentVars = (color: string, light: boolean): Record<string, string> => {
    const [r, g, b] = [1, 3, 5].map((index) => parseInt(color.slice(index, index + 2), 16));
    const hex = (channel: number) => Math.round(channel).toString(16).padStart(2, '0');
    const towards = light ? 0 : 255;
    const mixed = [r, g, b].map((channel) => channel + (towards - channel) * 0.2);

    return {
        '--accent': color,
        '--accent-hover': `#${mixed.map(hex).join('')}`,
        '--accent-glow': `rgba(${r}, ${g}, ${b}, ${light ? 0.2 : 0.3})`,
    };
};

export { accentVars, sanitizeAccent };
