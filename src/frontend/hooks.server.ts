import { withClerkHandler } from 'svelte-clerk/server';
import { sequence } from '@sveltejs/kit/hooks';
import { redirect } from '@sveltejs/kit';

export const handle = sequence(
    withClerkHandler(),
    async ({ event, resolve }) => {
        const { pathname } = event.url;
        
        // Define public routes
        const isPublicRoute = 
            pathname === '/' || 
            pathname.startsWith('/sign-in') || 
            pathname.startsWith('/sign-up') ||
            pathname.startsWith('/api/public'); // Fallback for public APIs if any

        // If it's a private route and no user is logged in, redirect to sign-in
        if (!isPublicRoute && !event.locals.auth?.userId) {
            throw redirect(307, `/sign-in?redirect_url=${pathname}`);
        }

        return resolve(event);
    }
);
