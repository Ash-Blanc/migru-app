<script lang="ts">
    import { Play, Pause, Music, Wind, Heart, Waves } from 'lucide-svelte';
    import { fade, fly, scale } from 'svelte/transition';
    import { clsx } from 'clsx';

    let isPlaying = false;
    let breathPhase: 'inhale' | 'hold' | 'exhale' = 'inhale';
    let isBreathingMode = false;
    
    function toggleBreathing() {
      isBreathingMode = !isBreathingMode;
    }
</script>

<div class="space-y-6 min-h-[calc(100vh-12rem)]">
  <!-- Immersive Breathing Orb Section -->
  <div 
    class={clsx(
      "relative flex flex-col items-center justify-center transition-all duration-700",
      isBreathingMode ? "py-12 sm:py-20" : "py-8 sm:py-12"
    )}
    in:fade={{ duration: 600 }}
  >
    <!-- Full aura backdrop when in breathing mode -->
    {#if isBreathingMode}
      <div 
        class="fixed inset-0 bg-base-200/90 backdrop-blur-xl z-[-1]"
        in:fade={{ duration: 500 }}
      ></div>
    {/if}
    
    <!-- Breathing Orb - Gemini-inspired focal point -->
    <button 
      class="relative group cursor-pointer focus:outline-none"
      on:click={toggleBreathing}
    >
      <!-- Outer aura rings -->
      <div class={clsx(
        "absolute rounded-full border-2 border-primary/20 transition-all duration-1000",
        isBreathingMode ? "inset-[-24px] sm:inset-[-32px] animate-breathe" : "inset-[-12px] sm:inset-[-16px]"
      )}></div>
      <div class={clsx(
        "absolute rounded-full border border-primary/10 transition-all duration-1000",
        isBreathingMode ? "inset-[-48px] sm:inset-[-64px] animate-breathe" : "inset-[-24px] sm:inset-[-32px] opacity-50"
      )} style="animation-delay: 0.4s"></div>
      <div class={clsx(
        "absolute rounded-full border border-primary/5 transition-all duration-1000",
        isBreathingMode ? "inset-[-72px] sm:inset-[-96px] animate-breathe" : "inset-[-36px] sm:inset-[-48px] opacity-30"
      )} style="animation-delay: 0.8s"></div>
      
      <!-- Main orb with gradient -->
      <div class={clsx(
        "relative rounded-full bg-gradient-to-br from-primary/30 via-secondary/20 to-primary/10 flex items-center justify-center backdrop-blur-sm transition-all duration-700",
        isBreathingMode 
          ? "w-40 h-40 sm:w-56 sm:h-56 animate-breathe shadow-2xl shadow-primary/30" 
          : "w-32 h-32 sm:w-40 sm:h-40 group-hover:scale-105"
      )}>
        <!-- Highlight -->
        <div class="absolute inset-0 rounded-full bg-gradient-to-t from-transparent to-white/20"></div>
        
        <!-- Inner icon -->
        <div class={clsx(
          "rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg transition-all duration-700",
          isBreathingMode 
            ? "w-20 h-20 sm:w-28 sm:h-28 shadow-primary/40 animate-pulse-soft" 
            : "w-14 h-14 sm:w-20 sm:h-20 shadow-primary/30"
        )}>
          <Wind size={isBreathingMode ? 36 : 28} class="text-primary-content" />
        </div>
      </div>
    </button>
    
    <!-- Instructions -->
    <div class={clsx(
      "text-center mt-8 transition-all duration-500",
      isBreathingMode ? "opacity-100" : "opacity-70"
    )} in:fly={{ y: 10, duration: 400, delay: 200 }}>
      <h1 class={clsx(
        "font-bold mb-2 transition-all duration-500",
        isBreathingMode ? "text-2xl sm:text-3xl" : "text-xl sm:text-2xl"
      )}>
        {isBreathingMode ? 'Breathe' : 'Active Relief'}
      </h1>
      <p class="text-base-content/50 text-sm max-w-xs mx-auto leading-relaxed">
        {#if isBreathingMode}
          <span class="font-medium text-primary">Inhale 4</span> • 
          <span class="font-medium text-secondary">Hold 7</span> • 
          <span class="font-medium text-accent">Exhale 8</span>
        {:else}
          Tap the orb to begin breathing
        {/if}
      </p>
    </div>
    
    <!-- Exit button when in breathing mode -->
    {#if isBreathingMode}
      <button 
        class="mt-8 btn btn-ghost btn-sm rounded-full text-xs opacity-50 hover:opacity-100"
        on:click={toggleBreathing}
        in:fade={{ duration: 300, delay: 500 }}
      >
        Tap to exit
      </button>
    {/if}
  </div>

  <!-- Tools Grid (hidden in breathing mode, simplified) -->
  {#if !isBreathingMode}
    <div class="space-y-3" in:fly={{ y: 20, duration: 400 }}>
      <h3 class="text-xs font-semibold uppercase tracking-wider opacity-50 px-1">Relief Tools</h3>
      
      <div class="grid grid-cols-3 gap-3">
        <!-- Binaural Beats -->
        <button 
          class={clsx(
            "flex flex-col items-center gap-2 p-4 rounded-2xl glass-ethereal transition-all duration-300 hover:scale-105 active:scale-95",
            isPlaying && "ring-2 ring-secondary shadow-lg shadow-secondary/20"
          )}
          on:click={() => isPlaying = !isPlaying}
        >
          <div class={clsx(
            "p-3 rounded-xl transition-all duration-300",
            isPlaying ? "bg-secondary text-secondary-content" : "bg-secondary/10 text-secondary"
          )}>
            <Music size={20} />
          </div>
          <span class="text-xs font-medium opacity-70">Beats</span>
          {#if isPlaying}
            <span class="absolute top-2 right-2 w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
          {/if}
        </button>

        <!-- Guided Meditation -->
        <button class="flex flex-col items-center gap-2 p-4 rounded-2xl glass-ethereal transition-all duration-300 hover:scale-105 active:scale-95">
          <div class="p-3 rounded-xl bg-accent/10 text-accent">
            <Heart size={20} />
          </div>
          <span class="text-xs font-medium opacity-70">Meditate</span>
        </button>
        
        <!-- White Noise -->
        <button class="flex flex-col items-center gap-2 p-4 rounded-2xl glass-ethereal transition-all duration-300 hover:scale-105 active:scale-95">
          <div class="p-3 rounded-xl bg-info/10 text-info">
            <Waves size={20} />
          </div>
          <span class="text-xs font-medium opacity-70">Sounds</span>
        </button>
      </div>
    </div>
  {/if}
</div>
