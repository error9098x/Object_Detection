# Install Tailwind 
npm install axios tailwindcss@latest postcss@latest autoprefixer@latest
# Config:
npx tailwindcss init -p
# tailwind config.js
module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
# src/index.css
@tailwind base;
@tailwind components;
@tailwind utilities;