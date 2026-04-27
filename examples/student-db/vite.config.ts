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

import { defineConfig, type UserConfig } from 'vite';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const loadSSLCertificate = (certPath: string, keyPath: string): { cert: Buffer; key: Buffer } | null => {
    try {
        return {
            cert: readFileSync(certPath),
            key: readFileSync(keyPath),
        };
    } catch (error) {
        console.warn('Failed to load SSL certificates, HTTPS disabled:', error instanceof Error ? error.message : 'Unknown error');
        return null;
    }
};

export const getBaseViteConfig = (): UserConfig => ({
    plugins: [react(), eslint()],
    resolve: {
        alias: {
            '@': resolve(__dirname, 'src'),
            '@teatype/api': resolve(__dirname, '../../ts/api'),
            '@teatype/apps': resolve(__dirname, '../../ts/apps'),
            '@teatype/baseconfig': resolve(__dirname, '../../ts/baseconfig'),
            '@teatype/components': resolve(__dirname, '../../ts/components'),
            '@teatype/hooks': resolve(__dirname, '../../ts/hooks'),
            '@teatype/icons': resolve(__dirname, '../../ts/icons'),
            '@teatype/style': resolve(__dirname, '../../ts/style'),
            '@teatype/toolkit': resolve(__dirname, '../../ts/toolkit'),
        },
    },
    css: {
        preprocessorOptions: {
            scss: {
                additionalData: `@use "${resolve(__dirname, '../../ts/style/globvars').replace(/\\/g, '/')}" as *;\n`,
            },
        },
    },
    server: {
        cors: true,
        host: '0.0.0.0',
        port: 5173,
        open: false,
    },
});

export default defineConfig(getBaseViteConfig());