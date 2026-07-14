import { Plus_Jakarta_Sans } from 'next/font/google'
//import { Roboto } from 'next/font/google'

import '@/styles/globals.css'

import type { AppProps } from 'next/app'

/*
const roboto = Roboto({
  weight: ['400', '700'],
  style: ['normal', 'italic'],
  subsets: ['latin'],
// CLS!!!  display: 'swap',
  variable: '--font-roboto', // dla zmiennych CSS
})
*/
const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  display: 'swap',
  preload: true,
  //  fallback: ['system-ui', 'arial', 'sans-serif'],
  //  adjustFontFallback: true, // automatycznie dostosowuje rozmiar dla fallback font
})

export default function App({ Component, pageProps }: AppProps) {
  return (
    //  <main className={`${plusJakartaSans.className} ${roboto.className}`}>
    <div className={`${plusJakartaSans.className}`}>
      <Component {...pageProps} />
    </div>
  )
}
