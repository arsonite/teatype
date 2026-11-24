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

// Lines of text that start at the left, the middle, the right or both edges
const LINES = {
    left: ['M4 6h16', 'M4 12h10', 'M4 18h14'],
    center: ['M4 6h16', 'M7 12h10', 'M5 18h14'],
    right: ['M4 6h16', 'M10 12h10', 'M6 18h14'],
    justify: ['M4 6h16', 'M4 12h16', 'M4 18h16'],
};

const TextAlignIcon = ({ align }: { align: keyof typeof LINES }) => (
    <svg viewBox='0 0 24 24' width='1em' height='1em' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' aria-hidden='true'>
        {LINES[align].map((line) => (
            <path key={line} d={line} />
        ))}
    </svg>
);

export default TextAlignIcon;

export { TextAlignIcon };
