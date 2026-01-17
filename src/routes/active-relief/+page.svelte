<script lang="ts">
  import { goto } from '$app/navigation';
  
  let isPlaying = true;
  let frequencyLayering = true;
  let isMuted = false;
</script>

<div class="bg-base-100 min-h-screen flex flex-col">
  <!-- Header -->
  <header class="flex items-center justify-between px-6 py-6">
    <button on:click={() => goto('/')} class="btn btn-circle btn-ghost">
      <span class="material-symbols-outlined text-3xl">keyboard_arrow_down</span>
    </button>
    
    <div class="badge badge-lg bg-base-200 gap-2">
      <span class="material-symbols-outlined text-primary">waves</span>
      Acoustic Pacing Active
    </div>
    
    <div class="relative">
      <div class="absolute inset-0 bg-primary/20 rounded-full animate-ping"></div>
      <button class="btn btn-circle btn-ghost text-primary">
        <span class="material-symbols-outlined text-2xl">mic</span>
      </button>
    </div>
  </header>

  <!-- Breathing Orb -->
  <main class="flex-1 flex flex-col items-center justify-center gap-12 px-6">
    <div class="relative w-72 h-72">
      <div class="absolute inset-0 bg-primary/10 rounded-full animate-ripple"></div>
      <div class="absolute inset-0 bg-primary/10 rounded-full animate-ripple-delayed"></div>
      <div class="w-48 h-48 rounded-full bg-gradient-to-br from-primary/40 to-primary/10 blur-xl animate-breathe mx-auto"></div>
    </div>

    <div class="text-center space-y-2">
      <h1 class="text-4xl font-bold">Breathe with me...</h1>
      <p class="text-xl opacity-80">Inhale... 4... Exhale... 4...</p>
    </div>
  </main>

  <!-- Controls -->
  <footer class="px-6 pb-12 space-y-6 w-full max-w-md mx-auto">
    <!-- Toggle -->
    <div class="card bg-base-200 border border-base-300 p-5">
      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium">Frequency Layering</p>
          <p class="text-sm opacity-60">Enhances binaural depth</p>
        </div>
        <input type="checkbox" class="toggle toggle-primary" bind:checked={frequencyLayering} />
      </div>
    </div>

    <!-- Playback -->
    <div class="grid grid-cols-2 gap-4">
      <button on:click={() => isMuted = !isMuted} class="btn btn-circle btn-lg bg-base-200 border-base-300">
        <span class="material-symbols-outlined text-3xl">
          {isMuted ? 'volume_up' : 'volume_off'}
        </span>
      </button>
      <button on:click={() => isPlaying = !isPlaying} class="btn btn-circle btn-lg bg-primary/20 border-primary/30">
        <span class="material-symbols-outlined text-4xl text-primary-content">
          {isPlaying ? 'pause' : 'play_arrow'}
        </span>
      </button>
    </div>
  </footer>
</div>