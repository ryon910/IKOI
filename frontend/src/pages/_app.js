// src/pages/_app.js
import '../styles/globals.css'; // グローバル CSS
import RootLayout from '../components/RootLayout'; 

export default function MyApp({ Component, pageProps }) {
  return (
    <RootLayout>
      <Component {...pageProps} />
    </RootLayout>
  );
}
