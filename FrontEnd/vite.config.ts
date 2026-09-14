import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// macOS AirPlay 占 5000 时：API_TARGET=http://localhost:5001 npm run dev
const apiTarget = process.env.API_TARGET || 'http://localhost:5000';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    proxy: {
      '/api': {
        target: apiTarget,
        changeOrigin: true,
      },
    },
  },
});
