<script>
    import { Play, Pause, Music, Wind } from 'lucide-svelte';
    import { fade } from 'svelte/transition';

    let isPlaying = false;
</script>

<div class="space-y-6" in:fade>
    <div class="text-center py-8">
        <div class="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
            <Wind size={48} class="text-primary" />
        </div>
        <h1 class="text-3xl font-bold mb-2">Active Relief</h1>
        <p class="opacity-60 max-w-xs mx-auto">Focus on your breathing. Inhale for 4, hold for 7, exhale for 8.</p>
    </div>

    <!-- Tools Grid -->
    <div class="grid grid-cols-1 gap-4">
        <div class="card bg-base-100 border border-base-200 shadow-sm">
            <div class="card-body p-4 flex-row items-center gap-4">
                <div class="bg-secondary/10 p-3 rounded-xl text-secondary">
                    <Music size={24} />
                </div>
                <div class="flex-1">
                    <h3 class="font-bold">Binaural Beats</h3>
                    <p class="text-xs opacity-60">Delta waves for pain relief</p>
                </div>
                <button class="btn btn-circle btn-sm btn-ghost" on:click={() => isPlaying = !isPlaying}>
                    {#if isPlaying}
                        <Pause size={20} />
                    {:else}
                        <Play size={20} />
                    {/if}
                </button>
            </div>
        </div>

        <div class="card bg-base-100 border border-base-200 shadow-sm">
            <div class="card-body p-4 flex-row items-center gap-4">
                <div class="bg-accent/10 p-3 rounded-xl text-accent">
                    <Wind size={24} />
                </div>
                <div class="flex-1">
                    <h3 class="font-bold">Guided Meditation</h3>
                    <p class="text-xs opacity-60">10 min body scan</p>
                </div>
                <button class="btn btn-circle btn-sm btn-ghost">
                    <Play size={20} />
                </button>
            </div>
        </div>
    </div>
</div>
