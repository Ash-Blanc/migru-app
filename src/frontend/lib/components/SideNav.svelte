<script lang="ts">
  import { page } from '$app/stores';
  import { Home, PlusCircle, ShieldAlert, Settings, Sparkles, Mic } from 'lucide-svelte';
  import { agentState, humeClient, isAgentOpen } from '$lib/stores';
  import { clsx } from 'clsx';
  
  const navItems = [
    { href: '/', icon: Home, label: 'Forecast' },
    { href: '/log', icon: PlusCircle, label: 'Log' },
    { href: '/active-relief', icon: ShieldAlert, label: 'Relief' }
  ];

  function handleVoiceClick() {
    if ($agentState === 'disconnected') {
      humeClient.connect();
    } else {
      // Toggle visibility if already connected
      $isAgentOpen = !$isAgentOpen;
    }
  }
</script>

<aside class="hidden lg:flex flex-col w-64 fixed left-0 top-0 h-screen z-50 overflow-hidden">
  <!-- Simple glass background -->
  <div class="absolute inset-0 bg-base-100/90 backdrop-blur-xl border-r border-base-content/5"></div>
  
  <!-- Content -->
  <div class="relative flex flex-col h-full">
    <!-- Logo Section -->
    <div class="p-6 flex items-center gap-3">
      <!-- Logo orb -->
      <div class="relative w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg shadow-primary/20">
        <svg class="w-6 h-6 text-primary-content" viewBox="0 0 100 114.42231082293117">
          <g transform="translate(-17.81291764397167, -10.601765466045661) scale(1.3562447978815297)" stroke="currentColor" fill="currentColor">
            <g xmlns="http://www.w3.org/2000/svg">
              <path d="M86.867,61.94c0-6.294-5.812-11.414-12.955-11.414c-0.001,0-0.003,0-0.004,0v-21.88   C73.908,17.161,63.182,7.817,50,7.817s-23.908,9.344-23.908,20.829v21.88c-0.001,0-0.003,0-0.004,0   c-7.143,0-12.954,5.12-12.954,11.414c0,3.574,1.884,6.891,5.026,9.031c-0.48,1.209-0.729,2.489-0.729,3.779   c0,6.294,5.812,11.415,12.954,11.415c2.634,0,5.146-0.692,7.261-1.96c1.659,4.62,6.57,7.979,12.354,7.979   s10.695-3.358,12.354-7.979c2.115,1.268,4.626,1.96,7.261,1.96c7.144,0,12.955-5.121,12.955-11.415c0-1.29-0.249-2.569-0.73-3.779   C84.983,68.831,86.867,65.514,86.867,61.94z M78.337,68.379l-2.062,0.977l1.238,1.916c0.7,1.084,1.056,2.254,1.056,3.478   c0,4.088-4.018,7.415-8.955,7.415c-2.851,0-5.471-1.101-7.188-3.019l-3.654-4.084l0.165,5.478c0.002,0.076,0.008,0.151,0.016,0.229   c0,4.088-4.017,7.415-8.954,7.415s-8.954-3.326-8.952-7.418l0.237-5.767l-3.712,4.146c-1.718,1.919-4.338,3.02-7.188,3.02   c-4.938,0-8.954-3.326-8.954-7.415c0-1.225,0.355-2.395,1.056-3.477l1.239-1.916l-2.063-0.978   c-2.794-1.324-4.529-3.792-4.529-6.439c0-4.088,4.017-7.414,8.954-7.414c0.546,0,1.099,0.046,1.689,0.14l2.314,0.368V28.646   c0-9.279,8.931-16.829,19.908-16.829s19.908,7.549,19.908,16.829v26.388l2.314-0.368c0.582-0.093,1.15-0.14,1.689-0.14   c4.938,0,8.955,3.326,8.955,7.414C82.867,64.587,81.131,67.055,78.337,68.379z"></path>
              <path d="M41.338,26.223c-0.864,0-1.571,0.707-1.571,1.571v7.107c0,0.864,0.707,1.571,1.571,1.571   s1.571-0.707,1.571-1.571v-7.107C42.909,26.93,42.202,26.223,41.338,26.223z"></path>
              <path d="M58.661,26.223c-0.864,0-1.571,0.707-1.571,1.571v7.107c0,0.864,0.707,1.571,1.571,1.571   s1.571-0.707,1.571-1.571v-7.107C60.232,26.93,59.525,26.223,58.661,26.223z"></path>
            </g>
          </g>
        </svg>
      </div>
      
      <div>
        <h1 class="text-xl font-bold gradient-text">MIGRU</h1>
        <p class="text-[10px] text-base-content/40 font-medium tracking-widest uppercase">Migraine Relief</p>
      </div>
    </div>
    
    <!-- Navigation -->
    <nav class="flex-1 px-3 space-y-1">
      {#each navItems as item}
        {@const isActive = $page.url.pathname === item.href}
        <a
          href={item.href}
          class={clsx(
            "group flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-300",
            isActive 
              ? "bg-primary text-primary-content shadow-lg shadow-primary/20" 
              : "text-base-content/50 hover:text-base-content hover:bg-base-content/5"
          )}
        >
          <svelte:component this={item.icon} size={20} strokeWidth={isActive ? 2.5 : 2} />
          <span class={clsx("font-medium text-sm", isActive && "font-semibold")}>
            {item.label}
          </span>
        </a>
      {/each}
      
      <!-- Desktop Voice Agent Trigger -->
       <button
          on:click={handleVoiceClick}
          class={clsx(
            "group flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-300 w-full text-left",
            $agentState !== 'disconnected' 
              ? "bg-gradient-to-r from-primary/10 to-secondary/10 text-primary border border-primary/20" 
              : "text-base-content/50 hover:text-base-content hover:bg-base-content/5"
          )}
        >
           <div class={clsx(
               "relative flex items-center justify-center w-5 h-5 transition-transform",
                $agentState !== 'disconnected' && "scale-110"
           )}>
               {#if $agentState !== 'disconnected'}
                    <span class="absolute inset-0 rounded-full bg-primary/20 animate-ping"></span>
               {/if}
               <Mic size={20} class={clsx($agentState !== 'disconnected' && "text-primary")} />
           </div>
          <span class={clsx("font-medium text-sm", $agentState !== 'disconnected' && "font-semibold")}>
            AI Assistant
          </span>
        </button>
    </nav>
    
    <!-- Footer / Settings -->
    <div class="p-3 border-t border-base-content/5">
      <a 
        href="/settings" 
        class={clsx(
          "flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-300",
          $page.url.pathname === '/settings' 
            ? "bg-base-content/10 text-base-content font-semibold" 
            : "text-base-content/50 hover:text-base-content hover:bg-base-content/5"
        )}
      >
        <Settings size={20} strokeWidth={$page.url.pathname === '/settings' ? 2.5 : 2} />
        <span class="font-medium text-sm">Settings</span>
      </a>
      
      <!-- Version badge -->
      <div class="mt-3 px-4 flex items-center gap-2 text-[10px] text-base-content/30">
        <Sparkles size={10} />
        <span>v1.0.0 • Beta</span>
      </div>
    </div>
  </div>
</aside>