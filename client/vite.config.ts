import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// TODO: Uncomment when testing
export default defineConfig({
	plugins: [sveltekit()],
	server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000/api',  // Flask server
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});

// export default defineConfig({
// 	plugins: [sveltekit()],
// });
