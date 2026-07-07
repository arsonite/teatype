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

// Components
import { TeaIcon } from '../components';

// Types
import type { iTeaIconProps } from '../components/TeaIcon';

const XIcon: React.FC<iTeaIconProps> = (props) => {
    return (
        <TeaIcon {...props}>
            <svg viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2'>
                <path d='M18 6L6 18M6 6l12 12' />
            </svg>
        </TeaIcon>
    );
};

export default XIcon;

export { XIcon };
