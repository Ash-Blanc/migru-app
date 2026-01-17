<script lang="ts">
  import { goto } from '$app/navigation';
  export let title: string = '';
  export let showBack: boolean = false;
  export let onBack: () => void = () => history.back();
</script>

<div class="navbar bg-base-100/50 backdrop-blur sticky top-0 z-40 px-4 min-h-16">
  <div class="navbar-start">
    {#if showBack}
      <button on:click={onBack} class="btn btn-circle btn-ghost btn-sm">
        <span class="material-symbols-outlined">arrow_back</span>
      </button>
    {/if}
  </div>
  
  <div class="navbar-center">
    <h2 class="text-lg font-bold">{title}</h2>
  </div>
  
  <div class="navbar-end">
    <button on:click={() => goto('/settings')} class="btn btn-circle btn-ghost btn-sm md:hidden">
      <span class="material-symbols-outlined">settings</span>
    </button>
  </div>
</div>