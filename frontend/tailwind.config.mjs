/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}', // Importante: escanea tus archivos Astro y HTML
    './public/**/*.html', // Si tienes HTML estático en public que usa Tailwind
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};