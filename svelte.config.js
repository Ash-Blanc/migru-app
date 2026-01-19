import adapter from '@sveltejs/adapter-vercel';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: adapter({
			runtime: 'nodejs20.x'
		}),
		// Custom directory structure
		files: {
			assets: 'src/frontend/static',
			lib: 'src/frontend/lib',
			routes: 'src/frontend/routes',
			appTemplate: 'src/frontend/app.html'
		}
	}
};

export default config;
