<script>
    import "../app.css";
    import BottomNav from "$lib/components/BottomNav.svelte";
    import SideNav from "$lib/components/SideNav.svelte";
    import TopAppBar from "$lib/components/TopAppBar.svelte";
    import VoiceAgent from "$lib/components/VoiceAgent.svelte";
</script>

<div class="min-h-screen flex flex-col lg:flex-row font-sans text-base-content selection:bg-primary/30 selection:text-primary-content">
    <!-- Ambient Background -->
    <div class="ambient-bg"></div>
    
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
    
    <!-- Mobile/Tablet Bottom Nav (hidden on lg screens) -->
    <div class="lg:hidden">
        <BottomNav />
    </div>
</div>
