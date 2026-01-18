<script lang="ts">
  import { agentState, agentMessage, humeClient, isAgentOpen } from '$lib/stores';
  import { Mic, Loader2, X, Sparkles } from 'lucide-svelte';
  import { clsx } from 'clsx';
  import { fade, fly, scale } from 'svelte/transition';

  function handleMicClick() {
    humeClient.toggleListening();
  }
  
  // Visualizer bars generation
  const bars = Array(5).fill(0);
</script>

<!-- Voice Agent Panel (No floating trigger, now controlled by BottomNav) -->

{#if $isAgentOpen && $agentState !== 'disconnected'}
  <!-- Chat Interface Overlay (Fixed at bottom, above nav) -->
  <div 
    class="fixed bottom-24 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none"
  >
    <div 
      transition:fly={{ y: 50, duration: 500, opacity: 0 }}
      class="pointer-events-auto w-full max-w-sm"
    >
      <div class="relative rounded-[2rem] glass-warm overflow-hidden shadow-glow-warm border border-white/20">
        
        <!-- Animated Background Mesh -->
        <div class="absolute inset-0 opacity-30 pointer-events-none">
            <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-white/10 to-transparent"></div>
            {#if $agentState === 'listening'}
                <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-32 h-32 bg-red-400/20 rounded-full blur-3xl animate-pulse"></div>
            {:else if $agentState === 'speaking'}
                 <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-32 h-32 bg-blue-400/20 rounded-full blur-3xl animate-pulse"></div>
            {/if}
        </div>

        <div class="relative p-6">
          <!-- Header -->
          <div class="flex justify-between items-center mb-6">
            <div class="flex items-center gap-2.5">
              <div class="relative">
                 <div class={clsx(
                    "w-2.5 h-2.5 rounded-full transition-all duration-500",
                    {
                      "bg-red-400 shadow-[0_0_10px_rgba(248,113,113,0.5)]": $agentState === 'listening',
                      "bg-blue-400 shadow-[0_0_10px_rgba(96,165,250,0.5)]": $agentState === 'processing',
                      "bg-green-400 shadow-[0_0_10px_rgba(74,222,128,0.5)]": $agentState === 'speaking',
                      "bg-gray-400": $agentState === 'idle'
                    }
                  )}></div>
                  {#if $agentState !== 'idle'}
                    <div class={clsx(
                        "absolute inset-0 rounded-full animate-ping opacity-75",
                         {
                           "bg-red-400": $agentState === 'listening',
                           "bg-blue-400": $agentState === 'processing',
                           "bg-green-400": $agentState === 'speaking'
                         }
                    )}></div>
                  {/if}
              </div>
              
              <span class="text-xs font-semibold tracking-wide uppercase opacity-50">
                {#if $agentState === 'listening'}Listening
                {:else if $agentState === 'processing'}Thinking
                {:else if $agentState === 'speaking'}Speaking
                {:else}Active{/if}
              </span>
            </div>
            
            <button 
              on:click={() => $isAgentOpen = false} 
              class="btn btn-ghost btn-xs btn-circle opacity-40 hover:opacity-100 hover:bg-black/5 transition-all"
            >
              <X size={16} />
            </button>
          </div>

          <!-- Agent Output / Visualizer Area -->
          <div class="min-h-[80px] mb-6 flex flex-col justify-center">
            {#if $agentMessage}
              <p class="text-[0.9375rem] leading-relaxed font-medium text-center" in:fade={{ duration: 300 }}>
                "{$agentMessage}"
              </p>
            {:else}
              <div class="flex flex-col items-center gap-3 opacity-40 py-2">
                <div class="flex gap-1 h-8 items-end">
                    {#each bars as _, i}
                        <div 
                            class="w-1 bg-current rounded-full animate-music" 
                            style="height: 40%; animation-delay: {i * 0.1}s; animation-duration: 0.8s"
                        ></div>
                    {/each}
                </div>
                <span class="text-xs font-medium tracking-wide">Ready to help</span>
              </div>
            {/if}
          </div>

          <!-- Interaction Area -->
          <div class="flex justify-center items-center gap-6">
            
             <!-- Decorative side buttons (optional for future features) -->
             <div class="w-8"></div> 

            <!-- Mic Button (Main Interaction) -->
            <button 
              on:click={handleMicClick}
              class={clsx(
                "relative group flex items-center justify-center w-16 h-16 rounded-full transition-all duration-500",
                $agentState === 'listening'
                  ? "bg-red-500 text-white shadow-lg shadow-red-500/30 scale-110" 
                  : "bg-white text-gray-800 shadow-xl shadow-black/5 hover:scale-105"
              )}
            >
              <!-- Ripple effect when listening -->
               {#if $agentState === 'listening'}
                <span class="absolute inset-0 rounded-full border border-white/30 animate-ripple"></span>
                <span class="absolute inset-0 rounded-full border border-white/20 animate-ripple-delayed"></span>
               {/if}

              {#if $agentState === 'processing'}
                <Loader2 class="w-6 h-6 animate-spin opacity-80" />
              {:else}
                <Mic class={clsx(
                    "w-6 h-6 transition-transform duration-300", 
                    $agentState === 'listening' ? "scale-110" : "group-hover:scale-110"
                )} />
              {/if}
            </button>
            
            <div class="w-8"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <style>
      @keyframes music {
          0%, 100% { height: 30%; opacity: 0.5; }
          50% { height: 100%; opacity: 1; }
      }
      .animate-music {
          animation: music 1s ease-in-out infinite;
      }
  </style>
{/if}
