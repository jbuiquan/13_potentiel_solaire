import type { Config } from "tailwindcss";

export default {
  darkMode: "selector",
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        'sol-ok': "#FAEA5E",
        'sol-top': "#E19803",
        'sol-ko': "#FFFBD6",
		'BG-darkmode':"#221C3E",
		'light-green': "#E7FFD3",
		'gray': "#5D5B65",
		'dark-green': "#355917",
		'gray-light-bg': "#FAFAFA",
		'select': "#A29DB9",
      },
      fontFamily: {
        verdana: ["verdana", "open-sans"],
      },
	  fontSize:{
		sm: '0.875rem',
		base: '1rem',
		lg:'2rem',
		xl:'2.5rem',
	  },
	  lineHeight:{
		normal:'100%',
		md:'1.313rem',
		lg:'1.375rem',
		xl:'1.75rem',
		'2xl':'2.813rem',
	  },
	  letterSpacing: {
		sm: '-3%',
		lg: '50%',
	  },
      spacing: {
        xs: "0.5rem",
        sm: "1rem",
        md: "1.5rem",
        lg: "2rem",
        xl: "3rem",
      },
      borderRadius: {},
	  boxShadow: {
		'base': '0px 4px 4px 0px rgba(0, 0, 0, 0.25)',
	  }
    },
  },
  plugins: [],
} satisfies Config;
