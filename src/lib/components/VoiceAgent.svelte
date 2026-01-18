<script lang="ts">
  import { agentState, agentMessage, humeClient } from '$lib/stores';
  import { Mic, MicOff, Loader2, Radio } from 'lucide-svelte';
  import { clsx } from 'clsx';
  import { fade, fly } from 'svelte/transition';

  let isOpen = false;

  function toggleAgent() {
    if ($agentState === 'disconnected') {
      humeClient.connect();
      isOpen = true;
    } else {
      // If already connected, just toggle visibility or mute?
      // For now, let's treat the button as a "Summon/Dismiss"
      // But we probably want a separate "disconnect"
      // humeClient.disconnect();
      // isOpen = false;
      isOpen = !isOpen;
    }
  }

  function handleMicClick() {
    humeClient.toggleListening();
  }
</script>

<!-- Floating Action Button / Status Indicator -->
<div class="fixed bottom-20 right-4 z-50 flex flex-col items-end gap-4 pointer-events-none">
  
  {#if isOpen && $agentState !== 'disconnected'}
    <!-- Chat Bubble / Agent Interface -->
    <div 
      transition:fly={{ y: 20, duration: 300 }}
      class="pointer-events-auto bg-base-100 shadow-xl rounded-2xl w-80 p-4 border border-base-200"
    >
      <!-- Header -->
      <div class="flex justify-between items-center mb-4">
        <div class="flex items-center gap-2">
            <div class={clsx("w-2 h-2 rounded-full animate-pulse", {
                "bg-red-500": $agentState === 'listening',
                "bg-blue-500": $agentState === 'processing',
                "bg-green-500": $agentState === 'speaking',
                "bg-gray-400": $agentState === 'idle'
            })}></div>
            <span class="text-sm font-semibold opacity-70">
                {#if $agentState === 'listening'} Listening...
                {:else if $agentState === 'processing'} Thinking...
                {:else if $agentState === 'speaking'} Speaking...
                {:else} Ready
                {/if}
            </span>
        </div>
        <button on:click={() => isOpen = false} class="btn btn-ghost btn-xs btn-circle">✕</button>
      </div>

      <!-- Agent Output -->
      <div class="min-h-[60px] max-h-[150px] overflow-y-auto mb-4 text-sm">
        {#if $agentMessage}
          <p class="leading-relaxed">{$agentMessage}</p>
        {:else}
          <p class="opacity-50 italic">Waiting for connection...</p>
        {/if}
      </div>

      <!-- Controls -->
      <div class="flex justify-center">
        <button 
            on:click={handleMicClick}
            class={clsx("btn btn-circle btn-lg transition-all duration-300", {
                "btn-error shadow-[0_0_20px_rgba(239,68,68,0.5)] scale-110": $agentState === 'listening',
                "btn-primary": $agentState !== 'listening'
            })}
        >
            {#if $agentState === 'processing'}
                <Loader2 class="w-8 h-8 animate-spin" />
            {:else if $agentState === 'listening'}
                <Mic class="w-8 h-8" />
            {:else}
                <Mic class="w-8 h-8" />
            {/if}
        </button>
      </div>
    </div>
  {/if}

  <!-- Trigger Button -->
  <button 
    on:click={toggleAgent}
    class={clsx("pointer-events-auto btn btn-circle btn-lg shadow-lg transition-transform hover:scale-105", {
        "btn-neutral": $agentState === 'disconnected',
        "btn-primary": $agentState !== 'disconnected'
    })}
  >
    {#if $agentState === 'disconnected'}
        <Radio class="w-6 h-6" />
    {:else}
        <!-- Pulse effect when connected but closed -->
        <span class="absolute inline-flex h-full w-full rounded-full bg-primary opacity-20 animate-ping"></span>
        <div class="relative w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center text-white font-bold">
            M
        </div>
    {/if}
  </button>
</div>
