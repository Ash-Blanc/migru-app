<script lang="ts">
  import { toastStore } from '$lib/stores';
  import { fly } from 'svelte/transition';
  import { CheckCircle, AlertCircle, Info } from 'lucide-svelte';
  import { clsx } from 'clsx';
</script>

{#if $toastStore}
  <div 
    class="fixed top-6 left-1/2 -translate-x-1/2 z-[100] w-full max-w-sm px-4 pointer-events-none"
  >
    <div 
      in:fly={{ y: -20, duration: 300 }} 
      out:fly={{ y: -20, duration: 200 }}
      class={clsx(
        "pointer-events-auto flex items-center gap-3 p-4 rounded-2xl shadow-xl border backdrop-blur-md",
        $toastStore.type === 'success' && "bg-success/10 border-success/20 text-success",
        $toastStore.type === 'error' && "bg-error/10 border-error/20 text-error",
        $toastStore.type === 'info' && "bg-info/10 border-info/20 text-info"
      )}
    >
      {#if $toastStore.type === 'success'}
        <CheckCircle size={20} class="shrink-0" />
      {:else if $toastStore.type === 'error'}
        <AlertCircle size={20} class="shrink-0" />
      {:else}
        <Info size={20} class="shrink-0" />
      {/if}
      
      <p class="font-medium text-sm">{$toastStore.message}</p>
    </div>
  </div>
{/if}
