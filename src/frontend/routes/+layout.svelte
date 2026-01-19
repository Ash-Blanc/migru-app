<script>
    import "../app.css";
    import BottomNav from "$lib/components/BottomNav.svelte";
    import SideNav from "$lib/components/SideNav.svelte";
    import TopAppBar from "$lib/components/TopAppBar.svelte";
    import VoiceAgent from "$lib/components/VoiceAgent.svelte";
    import Toast from "$lib/components/Toast.svelte";
    import { ClerkProvider } from 'svelte-clerk';
    import { PUBLIC_CLERK_PUBLISHABLE_KEY } from '$env/static/public';

    export let data;

    if (typeof window !== 'undefined') {
        console.log("Migru: Initializing with key present:", !!PUBLIC_CLERK_PUBLISHABLE_KEY);
        console.log("Migru: Layout data:", data);
    }
</script>

<!-- Ambient Background (Always render) -->
<div class="ambient-bg"></div>

<div class="sr-only">Migru Layout Rendering</div>

<ClerkProvider {...data} publishableKey={PUBLIC_CLERK_PUBLISHABLE_KEY}>
<div class="min-h-screen flex flex-col lg:flex-row font-sans text-base-content selection:bg-primary/30 selection:text-primary-content">
    
    <!-- Desktop Sidebar (only on lg screens 1024px+) -->
    <SideNav />

    <div class="flex-1 flex flex-col lg:pl-64 transition-all duration-300">
        <!-- Top Bar -->
        <TopAppBar />
        
        <!-- Main Content -->
        <main class="relative flex-1 px-4 py-4 sm:py-6 pb-24 lg:pb-8 w-full max-w-4xl mx-auto">
            <slot />
        </main>
    </div>

    <VoiceAgent />
    <Toast />
    
    <!-- Mobile/Tablet Bottom Nav (hidden on lg screens) -->
    <div class="lg:hidden">
        <BottomNav />
    </div>
</div>
</ClerkProvider>
