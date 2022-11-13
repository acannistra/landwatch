/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ], theme: {
    extend: {
      colors: {
        gold: "#c09d29",
        onyx: "#32373b",
        wildblue: "#90a6c4",
        green: "#1f5c47",
        chestnut: "#9f402d"
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography')
  ],
}
