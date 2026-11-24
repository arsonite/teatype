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

// A page with a second, narrower column at its right
const WorkspaceIcon = () => (
    <svg viewBox='0 0 24 24' width='1em' height='1em' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' aria-hidden='true'>
        <rect x='3' y='4' width='18' height='16' rx='2' />
        <path d='M15 4v16' />
        <path d='M18 8h.01M18 12h.01M18 16h.01' />
    </svg>
);

export default WorkspaceIcon;

export { WorkspaceIcon };
