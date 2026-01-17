<script lang="ts">
  import { page } from '$app/stores';
  
  const navItems = [
    { href: '/', icon: 'home', label: 'Home' },
    { href: '/active-relief', icon: 'self_care', label: 'Relief' },
    { href: '/forecast', icon: 'insights', label: 'Forecast' }
  ];
</script>

<div class="dock dock-md fixed bottom-0 left-0 right-0 w-full z-50 md:hidden">
  {#each navItems as item}
    <a
      href={item.href}
      class="{($page.url.pathname === item.href) ? 'dock-active' : ''}"
    >
      <span class="material-symbols-outlined text-xl">{item.icon}</span>
      <span class="dock-label text-xs">{item.label}</span>
    </a>
  {/each}
</div>