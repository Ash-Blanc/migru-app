import type { LayoutServerLoad } from './$types';
import { buildClerkProps } from 'svelte-clerk/server';

export const prerender = false;

export const load: LayoutServerLoad = async ({ locals }) => {
	return {
		...buildClerkProps(locals.auth || {})
	};
};
