import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	resolve: {
		alias: {
			$lib: path.resolve('./src/frontend/lib')
		}
	},
	server: {
		fs: {
			allow: ['src/frontend']
		}
	}
});