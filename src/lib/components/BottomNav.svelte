<script lang="ts">
  import { Home, PlusCircle, ShieldAlert, Settings } from 'lucide-svelte';
  import { page } from '$app/stores';
  import { clsx } from 'clsx';
</script>

<div class="btm-nav btm-nav-lg bg-base-100 border-t border-base-200 z-40 pb-safe">
  <a href="/" class={clsx({ "active text-primary": $page.url.pathname === '/' })}>
    <Home size={24} />
    <span class="btm-nav-label text-xs">Forecast</span>
  </a>
  
  <a href="/log" class={clsx({ "active text-primary": $page.url.pathname.includes('/log') })}>
    <PlusCircle size={24} />
    <span class="btm-nav-label text-xs">Log</span>
  </a>

  <a href="/active-relief" class={clsx({ "active text-primary": $page.url.pathname.includes('/active-relief') })}>
    <ShieldAlert size={24} />
    <span class="btm-nav-label text-xs">Relief</span>
  </a>
</div>
