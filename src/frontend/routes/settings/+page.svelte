<script lang="ts">
  import { slide, fly, fade } from 'svelte/transition';
  import { get } from 'svelte/store';
  import { apiKeys, userTheme, notificationsEnabled } from '$lib/stores';
  import { Key, Bell, LogOut, ChevronRight, Palette, Check } from 'lucide-svelte';
  import { clsx } from 'clsx';
  
  let showApiKeys = false;

  // Local bindings for inputs
  let humeKey = get(apiKeys.humeKey);
  let humeSecret = get(apiKeys.humeSecret);
  let humeConfigId = get(apiKeys.humeConfigId);
  let geminiKey = get(apiKeys.geminiKey);
  let mistralKey = get(apiKeys.mistralKey);

  function saveKeys() {
    apiKeys.humeKey.set(humeKey);
    apiKeys.humeSecret.set(humeSecret);
    apiKeys.humeConfigId.set(humeConfigId);
    apiKeys.geminiKey.set(geminiKey);
    apiKeys.mistralKey.set(mistralKey);
    alert("Keys Saved.");
  }
</script>

<div class="space-y-6 pb-24">
  <!-- Header -->
  <div 
    class="text-center py-4"
    in:fly={{ y: 20, duration: 500 }}
  >
    <!-- Avatar -->
    <div class="relative inline-block mb-4">
      <div class="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-primary-content text-xl font-bold shadow-lg shadow-primary/20">
        AL
      </div>
      <div class="absolute bottom-0 right-0 w-4 h-4 rounded-full bg-success border-2 border-base-100"></div>
    </div>
    <h1 class="text-xl font-bold">Settings</h1>
    <p class="text-xs text-base-content/50 mt-1">Preferences & Config</p>
  </div>

  <!-- General Settings -->
  <div 
    class="rounded-2xl glass-ethereal overflow-hidden"
    in:fly={{ y: 20, duration: 500, delay: 100 }}
  >
    <!-- Notifications -->
    <label class="flex items-center justify-between p-4 cursor-pointer hover:bg-base-content/5 transition-colors group">
      <div class="flex items-center gap-3">
        <div class="p-2 rounded-xl bg-blue-500/10 text-blue-500">
          <Bell size={18} />
        </div>
        <div>
          <span class="font-medium text-sm">Notifications</span>
          <p class="text-xs text-base-content/40">Daily check-ins</p>
        </div>
      </div>
      <input 
        type="checkbox" 
        class="toggle toggle-primary toggle-sm" 
        bind:checked={$notificationsEnabled} 
      />
    </label>

    <div class="h-px bg-base-content/5"></div>

    <!-- Theme -->
    <div class="flex items-center justify-between p-4 group hover:bg-base-content/5 transition-colors">
      <div class="flex items-center gap-3">
        <div class="p-2 rounded-xl bg-purple-500/10 text-purple-500">
          <Palette size={18} />
        </div>
        <div>
          <span class="font-medium text-sm">Theme</span>
          <p class="text-xs text-base-content/40">Appearance</p>
        </div>
      </div>
      <select class="select select-sm select-ghost w-auto font-medium bg-transparent pr-6" bind:value={$userTheme}>
        <option value="light">Light (Nord)</option>
        <option value="dark">Dark (Sunset)</option>
        <option value="system">System</option>
      </select>
    </div>
  </div>

  <!-- API Keys (collapsed by default) -->
  <div 
    class="rounded-2xl glass-ethereal overflow-hidden"
    in:fly={{ y: 20, duration: 500, delay: 200 }}
  >
    <button 
      class="flex items-center justify-between p-4 w-full text-left hover:bg-base-content/5 transition-colors"
      on:click={() => showApiKeys = !showApiKeys}
    >
      <div class="flex items-center gap-3">
        <div class={clsx(
          "p-2 rounded-xl transition-all duration-300",
          showApiKeys ? "bg-amber-500 text-white" : "bg-amber-500/10 text-amber-500"
        )}>
          <Key size={18} />
        </div>
        <div>
          <span class="font-medium text-sm">API Keys</span>
          <p class="text-xs text-base-content/40">Voice & LLM config</p>
        </div>
      </div>
      <ChevronRight 
        size={16} 
        class={clsx(
          "opacity-40 transition-transform duration-300",
          showApiKeys && "rotate-90"
        )} 
      />
    </button>

    {#if showApiKeys}
      <div class="p-4 pt-0 space-y-4" transition:slide={{ duration: 200 }}>
        <div class="h-px bg-base-content/5"></div>
        
        <div class="space-y-3">
          <p class="text-[10px] font-bold text-base-content/30 uppercase tracking-widest">Hume AI</p>
          <input 
            type="password" 
            placeholder="API Key" 
            class="input input-sm h-10 bg-base-content/5 border-0 w-full rounded-xl" 
            bind:value={humeKey} 
          />
          <input 
            type="password" 
            placeholder="Secret Key" 
            class="input input-sm h-10 bg-base-content/5 border-0 w-full rounded-xl" 
            bind:value={humeSecret} 
          />
          <input 
            type="text" 
            placeholder="Config ID (Optional)" 
            class="input input-sm h-10 bg-base-content/5 border-0 w-full rounded-xl" 
            bind:value={humeConfigId} 
          />
        </div>

        <div class="space-y-3">
          <p class="text-[10px] font-bold text-base-content/30 uppercase tracking-widest">LLM Providers</p>
          <input 
            type="password" 
            placeholder="Gemini API Key" 
            class="input input-sm h-10 bg-base-content/5 border-0 w-full rounded-xl" 
            bind:value={geminiKey} 
          />
          <input 
            type="password" 
            placeholder="Mistral API Key" 
            class="input input-sm h-10 bg-base-content/5 border-0 w-full rounded-xl" 
            bind:value={mistralKey} 
          />
        </div>

        <button 
          class="btn btn-primary w-full rounded-xl h-11 font-semibold gap-2" 
          on:click={saveKeys}
        >
          <Check size={16} />
          Save Keys
        </button>
      </div>
    {/if}
  </div>

  <!-- Sign Out -->
  <div 
    class="rounded-2xl glass-ethereal overflow-hidden"
    in:fly={{ y: 20, duration: 500, delay: 300 }}
  >
    <button class="flex items-center gap-3 p-4 w-full text-left text-error hover:bg-error/5 transition-colors">
      <div class="p-2 rounded-xl bg-error/10 text-error">
        <LogOut size={18} />
      </div>
      <span class="font-medium text-sm">Sign Out</span>
    </button>
  </div>
  
  <!-- Version -->
  <p 
    class="text-center text-xs text-base-content/20 py-4 flex items-center justify-center gap-1.5"
    in:fade={{ duration: 400, delay: 400 }}
  >
    v1.0.0 • Build 2024.1
  </p>
</div>
