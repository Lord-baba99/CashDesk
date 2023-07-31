/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './templates/*.html',
    './node_modules/flowbite/**/*.js',
    './**/templates/*.html'
  ],
  theme: {
    darkMode: 'class',
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

