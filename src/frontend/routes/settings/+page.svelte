<script lang="ts">
  import { fade } from 'svelte/transition';
  
  let notificationsEnabled = true;
  let theme = "light";
</script>

<div class="space-y-6" in:fade>
  <h1 class="text-2xl font-bold">Settings</h1>

  <div class="card bg-base-100 border border-base-200 shadow-sm">
    <div class="card-body">
        <h2 class="card-title text-base">Preferences</h2>
        
        <div class="form-control">
            <label class="label cursor-pointer">
                <span class="label-text">Enable Notifications</span>
                <input type="checkbox" class="toggle toggle-primary" bind:checked={notificationsEnabled} />
            </label>
        </div>

        <div class="form-control">
            <label class="label">
                <span class="label-text">Theme</span>
            </label>
            <select class="select select-bordered" bind:value={theme}>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="system">System</option>
            </select>
        </div>
    </div>
  </div>

  <div class="card bg-base-100 border border-base-200 shadow-sm">
    <div class="card-body">
        <h2 class="card-title text-base">Account</h2>
        <button class="btn btn-outline btn-error btn-sm">Sign Out</button>
    </div>
  </div>
</div>
