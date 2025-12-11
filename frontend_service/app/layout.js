import './styles/globals.css';
import MainLayout from './main/MainLayout';

export const metadata = {
  title: 'Yuhnie ❤️!!'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <MainLayout>
          {children}
        </MainLayout>
      </body>
    </html>
  );
}
