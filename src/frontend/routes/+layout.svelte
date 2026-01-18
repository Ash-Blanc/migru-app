<script>
    import "../app.css";
    import BottomNav from "$lib/components/BottomNav.svelte";
    import TopAppBar from "$lib/components/TopAppBar.svelte";
    import VoiceAgent from "$lib/components/VoiceAgent.svelte";
</script>

<div class="min-h-screen bg-base-100 flex flex-col font-sans text-base-content selection:bg-primary selection:text-white">
    <TopAppBar />
    
    <main class="flex-1 px-4 py-6 pb-24 max-w-md mx-auto w-full">
        <slot />
    </main>

    <VoiceAgent />
    <BottomNav />
</div>
