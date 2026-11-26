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
import React, { useState, useEffect, useRef, createContext, useContext } from 'react';

// Icons
import { BackIcon, ChevronIcon, PlusIcon, XIcon } from '../icons';

// Utility
import { swipeLeft } from '@teatype/toolkit/gestures';

// Components
import { TeaHubLink, isEmbedded } from './TeaHubLink';
import { TeaButton } from './input/TeaButton';

// Style
import './style/TeaSidebar.scss';

const ACTION_THEMES = { primary: 'filled', secondary: 'default', danger: 'danger' } as const;

export type tTeaSidebarItem = {
    active?: boolean;
    icon?: React.ReactNode;
    id: string;
    meta?: string;
    subtitle?: string;
    title: string;
};

export type tTeaSidebarSection = {
    collapsible?: boolean;
    count?: number;
    defaultCollapsed?: boolean;
    id: string;
    items: tTeaSidebarItem[];
    title: string;
};

export type tTeaSidebarAction = {
    icon?: React.ReactNode;
    id: string;
    label: string;
    variant?: 'primary' | 'secondary' | 'danger';
    onClick: () => void;
};

export interface iTeaSidebarProps {
    children?: React.ReactNode;
    collapsedWidth?: number;
    expanded: boolean;
    expandedWidth?: number;
    emptyMessage?: string;
    footer?: React.ReactNode;
    // Where the "back to hub" link of an app that is embedded in a hub (homepie) points to, false leaves it out. Standalone apps never show it.
    hubHref?: string | false;
    toggleKey?: string;
    headerActions?: tTeaSidebarAction[];
    // A phone: expanded is then a sheet over everything, closed with an X or a swipe to the left
    mobile?: boolean;
    // Shown at the bottom of the collapsed sidebar, below a rule. Collapsed, the sidebar is a rail over the left edge of the page.
    rail?: React.ReactNode;
    sections?: tTeaSidebarSection[];
    showItemDelete?: boolean;
    // A string is shown as heading, a node takes its place in the header
    title?: React.ReactNode;
    onItemClick?: (sectionId: string, itemId: string) => void;
    onItemDelete?: (sectionId: string, itemId: string) => void;
    onToggle: () => void;
}

interface iTeaSidebarContextValue {
    expanded: boolean;
    onToggle: () => void;
}

const TeaSidebarContext = createContext<iTeaSidebarContextValue | null>(null);

export const useTeaSidebar = () => {
    const context = useContext(TeaSidebarContext);
    if (!context) {
        throw new Error('useTeaSidebar must be used within TeaSidebar');
    }
    return context;
};

interface tTeaSidebarSectionComponentProps {
    section: tTeaSidebarSection;
    showItemDelete?: boolean;
    onItemClick?: (itemId: string) => void;
    onItemDelete?: (itemId: string) => void;
}

const TeaSidebarSectionComponent: React.FC<tTeaSidebarSectionComponentProps> = ({
    section,
    showItemDelete,
    onItemClick,
    onItemDelete,
}) => {
    const [collapsed, setCollapsed] = useState(section.defaultCollapsed ?? false);

    return (
        <div className='tea-sidebar-section'>
            <div
                className={`tea-sidebar-section__header ${section.collapsible ? 'tea-sidebar-section__header--collapsible' : ''}`}
                onClick={() => section.collapsible && setCollapsed(!collapsed)}
            >
                <span className='tea-sidebar-section__title'>{section.title}</span>
                {section.count !== undefined && <span className='tea-sidebar-section__count'>{section.count}</span>}
                {section.collapsible && (
                    <span
                        className={`tea-sidebar-section__chevron ${collapsed ? '' : 'tea-sidebar-section__chevron--open'}`}
                    >
                        <ChevronIcon />
                    </span>
                )}
            </div>

            {!collapsed && (
                <div className='tea-sidebar-section__items'>
                    {section.items.length === 0 ? (
                        <div className='tea-sidebar-section__empty'>No items</div>
                    ) : (
                        section.items.map((item) => (
                            <div
                                key={item.id}
                                className={`tea-sidebar-item ${item.active ? 'tea-sidebar-item--active' : ''}`}
                                onClick={() => onItemClick?.(item.id)}
                                role='button'
                                tabIndex={0}
                                onKeyDown={(e) => e.key === 'Enter' && onItemClick?.(item.id)}
                            >
                                {item.icon && <span className='tea-sidebar-item__icon'>{item.icon}</span>}
                                <div className='tea-sidebar-item__content'>
                                    <div className='tea-sidebar-item__header'>
                                        <span className='tea-sidebar-item__title'>{item.title}</span>
                                        {showItemDelete && onItemDelete && (
                                            <TeaButton
                                                variant='borderless'
                                                theme='danger'
                                                size='xs'
                                                disableRipple
                                                className='tea-sidebar-item__delete'
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    onItemDelete(item.id);
                                                }}
                                                title='Delete'
                                            >
                                                <XIcon width='1em' height='1em' />
                                            </TeaButton>
                                        )}
                                    </div>
                                    {(item.subtitle || item.meta) && (
                                        <div className='tea-sidebar-item__meta'>
                                            {item.meta && <span className='tea-sidebar-item__date'>{item.meta}</span>}
                                            {item.subtitle && (
                                                <span className='tea-sidebar-item__subtitle'>{item.subtitle}</span>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );
};

export interface iTeaSidebarSettingsSection {
    id: string;
    label: string;
    children: React.ReactNode;
}

export interface iTeaSidebarSettingsProps {
    isOpen: boolean;
    isClosing?: boolean;
    sections: iTeaSidebarSettingsSection[];
}

export const TeaSidebarSettings: React.FC<iTeaSidebarSettingsProps> = ({ isOpen, isClosing, sections }) => {
    if (!isOpen) return null;

    return (
        <div className={`tea-sidebar-settings ${isClosing ? 'tea-sidebar-settings--closing' : ''}`}>
            {sections.map((section) => (
                <div key={section.id} className='tea-sidebar-settings__section'>
                    <span className='tea-sidebar-settings__label'>{section.label}</span>
                    {section.children}
                </div>
            ))}
        </div>
    );
};

export const TeaSidebarSlider: React.FC<{
    min: number;
    max: number;
    step?: number;
    value: number;
    onChange: (value: number) => void;
    unit?: string;
}> = ({ min, max, step = 1, value, onChange, unit = '' }) => (
    <div className='tea-sidebar-slider'>
        <input
            type='range'
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={(e) => onChange(Number(e.target.value))}
        />
        <span className='tea-sidebar-slider__value'>
            {value}
            {unit}
        </span>
    </div>
);

export const TeaSidebarToggle: React.FC<{
    checked: boolean;
    onChange: (checked: boolean) => void;
    label: string;
}> = ({ checked, onChange, label }) => (
    <div className='tea-sidebar-toggle'>
        <label>
            <input type='checkbox' checked={checked} onChange={(e) => onChange(e.target.checked)} />
            {label}
        </label>
    </div>
);

export const TeaSidebarButton: React.FC<{
    onClick: () => void;
    variant?: 'default' | 'danger';
    children: React.ReactNode;
}> = ({ onClick, variant = 'default', children }) => (
    <TeaButton fullWidth align='start' size='small' theme={variant === 'danger' ? 'danger' : 'default'} onClick={onClick}>
        {children}
    </TeaButton>
);

export const TeaSidebarButtonGroup: React.FC<{
    children: React.ReactNode;
}> = ({ children }) => <div className='tea-sidebar-btn-group'>{children}</div>;

export const TeaSidebar: React.FC<iTeaSidebarProps> = ({
    title,
    toggleKey,
    expanded,
    headerActions,
    sections,
    showItemDelete = true,
    footer,
    hubHref = '/',
    children,
    expandedWidth = 300,
    collapsedWidth = 44,
    mobile = false,
    rail,
    emptyMessage = 'No items yet',

    onItemClick,
    onItemDelete,
    onToggle,
}) => {
    const contextValue: iTeaSidebarContextValue = {
        expanded,
        onToggle,
    };
    const showHub = hubHref !== false && isEmbedded();

    // A ref, so that a render during the swipe does not restart it
    const toggleRef = useRef(onToggle);
    toggleRef.current = onToggle;
    useEffect(() => (mobile && expanded ? swipeLeft(() => toggleRef.current()) : undefined), [mobile, expanded]);

    const toggle = (
        <TeaButton
            variant='borderless'
            size='small'
            iconOnly
            disableRipple
            className='tea-sidebar__toggle'
            onClick={onToggle}
            title={expanded ? (mobile ? 'Close' : 'Collapse') : 'Expand'}
        >
            {expanded && mobile ? (
                <XIcon width='1.1em' height='1.1em' />
            ) : (
                <span className={`tea-sidebar__toggle-icon ${expanded ? '' : 'tea-sidebar__toggle-icon--flipped'}`}>
                    <BackIcon thin />
                </span>
            )}
            {toggleKey && <span className='tea-sidebar__key'>{toggleKey}</span>}
        </TeaButton>
    );

    return (
        <TeaSidebarContext.Provider value={contextValue}>
            <aside
                className={`tea-sidebar ${expanded ? 'tea-sidebar--expanded' : 'tea-sidebar--collapsed'} ${
                    mobile ? 'tea-sidebar--mobile' : ''
                }`}
                style={
                    {
                        '--tea-sidebar-expanded-width': `${expandedWidth}px`,
                        '--tea-sidebar-collapsed-width': `${collapsedWidth}px`,
                    } as React.CSSProperties
                }
            >
                <div className='tea-sidebar__header'>
                    {toggle}
                    {typeof title === 'string' ? <h2 className='tea-sidebar__title'>{title}</h2> : title}
                    {headerActions?.map((action) => (
                        <TeaButton
                            key={action.id}
                            size='small'
                            iconOnly
                            disableRipple
                            theme={ACTION_THEMES[action.variant || 'primary']}
                            className='tea-sidebar__action'
                            onClick={action.onClick}
                            title={action.label}
                        >
                            {action.icon || <PlusIcon />}
                        </TeaButton>
                    ))}
                </div>

                <div className='tea-sidebar__content'>
                    {children ? (
                        children
                    ) : sections ? (
                        sections.map((section) => (
                            <TeaSidebarSectionComponent
                                key={section.id}
                                section={section}
                                onItemClick={(itemId) => onItemClick?.(section.id, itemId)}
                                onItemDelete={(itemId) => onItemDelete?.(section.id, itemId)}
                                showItemDelete={showItemDelete}
                            />
                        ))
                    ) : (
                        <div className='tea-sidebar__empty'>{emptyMessage}</div>
                    )}
                </div>

                {(footer || showHub) && (
                    <div className='tea-sidebar__footer'>
                        {showHub && <TeaHubLink href={hubHref || undefined} />}
                        {footer}
                    </div>
                )}
            </aside>

            {!expanded && (
                <div
                    className='tea-rail-background'
                    style={{ '--tea-sidebar-collapsed-width': `${collapsedWidth}px` } as React.CSSProperties}
                />
            )}
            {!expanded && (
                <div
                    className='tea-rail'
                    style={{ '--tea-sidebar-collapsed-width': `${collapsedWidth}px` } as React.CSSProperties}
                >
                    {toggle}
                    {(rail || showHub) && (
                        <div className='tea-rail__bottom'>
                            <hr className='tea-rail__rule' />
                            {/* At the bottom like the footer of the open sidebar */}
                            {showHub && <TeaHubLink href={hubHref || undefined} variant='rail' />}
                            {rail}
                        </div>
                    )}
                </div>
            )}
        </TeaSidebarContext.Provider>
    );
};

export default TeaSidebar;
