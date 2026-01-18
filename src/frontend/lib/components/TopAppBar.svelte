<script>
    import { Bell, User } from 'lucide-svelte';
</script>

<div class="navbar bg-base-100/80 backdrop-blur-md sticky top-0 z-40 border-b border-base-200 px-4">
  <div class="flex-1">
    <a href="/" class="btn btn-ghost text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Migru</a>
  </div>
  <div class="flex-none gap-2">
    <button class="btn btn-ghost btn-circle">
      <div class="indicator">
        <Bell size={20} />
        <span class="badge badge-xs badge-primary indicator-item"></span>
      </div>
    </button>
    <div class="dropdown dropdown-end">
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
        <div class="w-9 rounded-full bg-neutral text-neutral-content flex items-center justify-center">
          <span class="text-xs">US</span>
        </div>
      </div>
      <ul tabindex="0" class="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52">
        <li><a href="/settings">Settings</a></li>
        <li><a>Logout</a></li>
      </ul>
    </div>
  </div>
</div>
