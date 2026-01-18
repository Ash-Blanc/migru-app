<script lang="ts">
  import { agentState, agentMessage, humeClient, isAgentOpen } from '$lib/stores';
  import { Mic, Loader2, X, Sparkles } from 'lucide-svelte';
  import { clsx } from 'clsx';
  import { fade, fly } from 'svelte/transition';

  function handleMicClick() {
    humeClient.toggleListening();
  }
</script>

<!-- Voice Agent Panel (No floating trigger, now controlled by BottomNav) -->

{#if $isAgentOpen && $agentState !== 'disconnected'}
  <!-- Chat Interface Overlay (Fixed at bottom, above nav) -->
  <div 
    class="fixed bottom-24 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none"
  >
    <div 
      transition:fly={{ y: 20, duration: 400 }}
      class="pointer-events-auto w-full max-w-sm"
    >
      <div class="relative rounded-3xl glass-ethereal overflow-hidden border border-primary/10 shadow-2xl">
        <div class="p-5">
          <!-- Header -->
          <div class="flex justify-between items-center mb-4">
            <div class="flex items-center gap-2">
              <div class={clsx(
                "w-2 h-2 rounded-full transition-colors duration-300",
                {
                  "bg-error animate-pulse": $agentState === 'listening',
                  "bg-blue-500 animate-pulse": $agentState === 'processing',
                  "bg-success": $agentState === 'speaking',
                  "bg-base-content/30": $agentState === 'idle'
                }
              )}></div>
              <span class="text-xs font-medium opacity-60">
                {#if $agentState === 'listening'}Listening...
                {:else if $agentState === 'processing'}Thinking...
                {:else if $agentState === 'speaking'}Speaking...
                {:else}Ready{/if}
              </span>
            </div>
            <button 
              on:click={() => $isAgentOpen = false} 
              class="btn btn-ghost btn-xs btn-circle opacity-50 hover:opacity-100"
            >
              <X size={14} />
            </button>
          </div>

          <!-- Agent Output -->
          <div class="min-h-[48px] max-h-[120px] overflow-y-auto mb-5">
            {#if $agentMessage}
              <p class="text-sm leading-relaxed" in:fade={{ duration: 200 }}>
                {$agentMessage}
              </p>
            {:else}
              <div class="flex items-center gap-2 text-xs opacity-40">
                <Sparkles size={12} />
                <span class="italic">Ask about your migraines...</span>
              </div>
            {/if}
          </div>

          <!-- Mic Button (Main Interaction) -->
          <div class="flex justify-center">
            <button 
              on:click={handleMicClick}
              class={clsx(
                "relative btn btn-circle btn-lg border-0 transition-all duration-300",
                $agentState === 'listening'
                  ? "bg-error text-white shadow-lg shadow-error/40 scale-110" 
                  : "bg-gradient-to-br from-primary to-secondary text-primary-content shadow-lg shadow-primary/30"
              )}
            >
              {#if $agentState === 'listening'}
                <span class="absolute inset-0 rounded-full bg-error/30 animate-ping"></span>
              {/if}
              
              {#if $agentState === 'processing'}
                <Loader2 class="w-6 h-6 animate-spin" />
              {:else}
                <Mic class="w-6 h-6 relative z-10" />
              {/if}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}
