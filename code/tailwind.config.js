/** @type {import('tailwindcss').Config} */
module.exports = {
  
  content: [
    './templates/**/*.html',
    './apps/**/*.py',
  ],

  theme: {
    extend: {},
  },

  // Adiciona o plugin do daisyUI
  plugins: [
    require("daisyui"),
  ],

  // Configuração do daisyUI 
  daisyui: {
    themes: ["pousada", "light", "dark"],  
  },
}
