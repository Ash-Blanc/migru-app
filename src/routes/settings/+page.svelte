<script lang="ts">
  import { settings, themes } from '$lib/stores';
  import { slide } from 'svelte/transition';

  let activeSection = 'profile';

  function capitalize(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
</script>

<div class="max-w-3xl mx-auto px-6 py-8 pb-24 md:pb-8">
  <h1 class="text-3xl font-bold mb-8">Settings</h1>

  <div class="grid gap-6">
    <!-- Profile Section -->
    <div class="card bg-base-100 border border-base-200 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-base-200 flex justify-between items-center bg-base-100/50">
        <h2 class="text-xl font-bold flex items-center gap-3">
          <span class="material-symbols-outlined text-primary">person</span>
          Profile
        </h2>
      </div>
      
      <div class="card-body p-6 gap-6">
        <div class="flex items-center gap-6">
          <div class="avatar placeholder">
            <div class="bg-neutral text-neutral-content rounded-full w-24">
              <span class="text-3xl">{ $settings.profile.name.charAt(0) }</span>
            </div>
          </div>
          <div class="flex-1 space-y-4">
             <div class="form-control w-full">
              <label class="label" for="profile-name">
                <span class="label-text">Display Name</span>
              </label>
              <input id="profile-name" type="text" bind:value={$settings.profile.name} class="input input-bordered w-full" />
            </div>
          </div>
        </div>
        
        <div class="form-control w-full">
          <label class="label" for="profile-email">
            <span class="label-text">Email Address</span>
          </label>
          <input id="profile-email" type="email" bind:value={$settings.profile.email} class="input input-bordered w-full" />
        </div>
      </div>
    </div>

    <!-- Appearance Section -->
    <div class="card bg-base-100 border border-base-200 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-base-200 bg-base-100/50">
        <h2 class="text-xl font-bold flex items-center gap-3">
          <span class="material-symbols-outlined text-secondary">palette</span>
          Appearance
        </h2>
      </div>
      
      <div class="card-body p-6">
        <p class="mb-4 text-sm opacity-70">Choose a theme that fits your vibe.</p>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {#each themes as theme}
            <button 
              class="btn h-auto py-4 flex flex-col gap-2 border-2 transition-all
              {$settings.theme === theme ? 'border-primary bg-base-200' : 'border-base-200 bg-base-100 hover:border-base-300'}"
              on:click={() => $settings.theme = theme}
            >
              <div data-theme={theme} class="w-full h-8 rounded bg-base-100 border border-base-content/10 shadow-sm grid grid-cols-4 overflow-hidden gap-1 p-1">
                <div class="bg-primary rounded-sm col-span-1"></div>
                <div class="bg-secondary rounded-sm col-span-1"></div>
                <div class="bg-accent rounded-sm col-span-1"></div>
                <div class="bg-neutral rounded-sm col-span-1"></div>
              </div>
              <span class="text-xs font-medium">{capitalize(theme)}</span>
            </button>
          {/each}
        </div>
      </div>
    </div>

    <!-- Notifications Section -->
    <div class="card bg-base-100 border border-base-200 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-base-200 bg-base-100/50">
        <h2 class="text-xl font-bold flex items-center gap-3">
          <span class="material-symbols-outlined text-accent">notifications</span>
          Notifications
        </h2>
      </div>
      
      <div class="card-body p-0">
        <div class="divide-y divide-base-200">
          <div class="flex items-center justify-between p-4 hover:bg-base-200/50 transition-colors">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-info/10 text-info flex items-center justify-center">
                <span class="material-symbols-outlined">water_drop</span>
              </div>
              <div>
                <p class="font-bold">Hydration Alerts</p>
                <p class="text-xs opacity-60">Reminders to drink water when pressure drops</p>
              </div>
            </div>
            <input type="checkbox" class="toggle toggle-info" bind:checked={$settings.notifications.hydration} />
          </div>

          <div class="flex items-center justify-between p-4 hover:bg-base-200/50 transition-colors">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-warning/10 text-warning flex items-center justify-center">
                <span class="material-symbols-outlined">storm</span>
              </div>
              <div>
                <p class="font-bold">Barometer Alerts</p>
                <p class="text-xs opacity-60">Notify when storm fronts approach</p>
              </div>
            </div>
            <input type="checkbox" class="toggle toggle-warning" bind:checked={$settings.notifications.barometer} />
          </div>

          <div class="flex items-center justify-between p-4 hover:bg-base-200/50 transition-colors">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-secondary/10 text-secondary flex items-center justify-center">
                <span class="material-symbols-outlined">bedtime</span>
              </div>
              <div>
                <p class="font-bold">Sleep Reminders</p>
                <p class="text-xs opacity-60">Suggestions for winding down</p>
              </div>
            </div>
            <input type="checkbox" class="toggle toggle-secondary" bind:checked={$settings.notifications.sleep} />
          </div>
        </div>
      </div>
    </div>

     <!-- Data Section -->
     <div class="card bg-base-100 border border-base-200 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-base-200 bg-base-100/50">
        <h2 class="text-xl font-bold flex items-center gap-3">
          <span class="material-symbols-outlined text-error">database</span>
          Data & Privacy
        </h2>
      </div>
      <div class="card-body p-6">
        <p class="text-sm mb-4">Manage your personal data stored on this device.</p>
        <div class="flex flex-wrap gap-3">
          <button class="btn btn-outline">
            <span class="material-symbols-outlined">download</span>
            Export Data
          </button>
          <button class="btn btn-outline btn-error">
            <span class="material-symbols-outlined">delete</span>
            Delete All Data
          </button>
        </div>
      </div>
    </div>

  </div>
</div>