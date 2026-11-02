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
import React from 'react';
import { useNavigate } from 'react-router-dom';

// Components
import { BackIcon } from '@teatype/icons';
import TeaButton, { iTeaButtonProps } from '../TeaButton';

const BackButton: React.FC<iTeaButtonProps> = (props) => {
    const navigate = useNavigate();

    return (
        <TeaButton
            disableRipple
            disableIconRotation
            size='small'
            variant='borderless'
            {...props}
            onClick={
                props.onClick !== undefined
                    ? props.onClick
                    : () => {
                          navigate(-1);
                      }
            }
        >
            <BackIcon />
        </TeaButton>
    );
};

export default BackButton;

export { BackButton };
