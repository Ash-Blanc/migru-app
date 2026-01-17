<script lang="ts">
  import '../app.css';
  import { browser } from '$app/environment';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import SideNav from '$lib/components/SideNav.svelte';
  
  if (browser) {
    const fonts = [
      { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
      { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossOrigin: 'anonymous' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap' }
    ];
    
    fonts.forEach(link => {
      const el = document.createElement('link');
      Object.entries(link).forEach(([k, v]) => el.setAttribute(k, v));
      document.head.appendChild(el);
    });
  }
</script>

<div class="md:pl-64 min-h-screen">
  <SideNav />
  <slot />
  <div class="h-20 md:hidden"></div>
</div>

<BottomNav />

<svelte:head>
  <meta name="theme-color" content="#ff4d00" />
</svelte:head>