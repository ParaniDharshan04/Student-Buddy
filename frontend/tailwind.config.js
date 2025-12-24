/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef9e7',
          100: '#fdf2c7',
          200: '#fbe58a',
          300: '#f9d24d',
          400: '#f7c020',
          500: '#d4a017',
          600: '#b8860b',
          700: '#8b6914',
          800: '#6b5416',
          900: '#5a4617',
        },
        dark: {
          50: '#f7f7f8',
          100: '#e3e4e6',
          200: '#c7c9cd',
          300: '#a4a7ae',
          400: '#7e828c',
          500: '#636773',
          600: '#4e515b',
          700: '#42444c',
          800: '#393a41',
          900: '#1a1b1e',
          950: '#0a0a0b',
        },
      },
    },
  },
  plugins: [],
}
