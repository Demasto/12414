import type {ThemeDefinition} from "vuetify";

// const blue2 = '#406C91'
const primaryLighten = '#3e72c2'
const primary = '#7f42e1'
const primaryDarken = '#324999'

const secondary = '#ffffff'

const black1 = '#272832'
const black2 = '#323139'
const black3 = '#37383E'
const black4 = '#4C4C52'

const background = '#F6F7F9'

const gray0 = '#F2F3F9'
const gray = '#E4E5ED'
const gray2 = '#E0E0E3'
const gray3 = '#CFCFD7'
const gray4 = '#B3B5C3'
const gray5 = '#7C7D86'

const red = '#D7484A'
const success = '#DFF8E9'

export const lightTheme: ThemeDefinition = {
    dark: false,
    colors: {
        surface: secondary,
        'on-surface': primary,
        background: background,
        'on-background': black4,

        primary: primary,
        'on-primary': secondary,

        secondary: secondary,
        'on-secondary': primary,

        // Дополнительные варианты (для outlined):
        'primary-lighten1': primaryLighten, // Используется как фон для outlined
        'primary-darken1': primaryDarken, // для hover

        'black-1': black1,
        'black-2': black2,
        'black-3': black3,
        'black-4': black4,

        gray: gray,
        'on-gray': primary,

        'gray-0': gray0,
        'gray-3': gray3,
        'gray-4': gray4,
        'gray-5': gray5,

        red: red,
        'on-red': secondary,

        success: success,
        warn: '#ff9800',
        error: red,
        'error-lighten1': '#ffe0e0',

        disabled: gray2,
        'on-disabled': '#b6b5b5',   // (если нужен текст другой)

        'on-surface-variant': primary,
        'surface-variant': gray,
    },
    variables: {
        'border-color': gray,
        'border-opacity': 0.4,
        'high-emphasis-opacity': 0.9,
        'medium-emphasis-opacity': 0.88,
        'disabled-opacity': 0.9,
        'hover-opacity': 0.08,
        'focus-opacity': 0,
        'selected-opacity': 0,
        'activated-opacity': 0.35,
        'pressed-opacity': 0.05,
        'theme-overlay-multiplier': 0.3,
    }
}