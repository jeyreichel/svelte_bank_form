/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './src/**/*.{html,js,svelte,ts}',
    ],
    theme: {
        extend: {
            colors: {
                'main-yellow': '#FBE13F',
                'main-orange': '#FFC15E',
                'regal-blue': '#243c5a',
                'main-black':'#34314F'
            }
        },
    },
    plugins: [require('flowbite/plugin')],
    darkMode: 'class',
}
