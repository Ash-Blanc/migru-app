<script lang="ts">
  import "../app.css";
  import { goto } from '$app/navigation';
  import TopAppBar from '$lib/components/TopAppBar.svelte';
  import ForecastCard from '$lib/components/ForecastCard.svelte';
  import BottomNav from '$lib/components/BottomNav.svelte';
  import { settings, appState } from '$lib/stores';
  
  const currentTime = new Date().getHours();
  const greeting = currentTime < 12 ? "Good morning" : currentTime < 18 ? "Good afternoon" : "Good evening";

  // Helper to get status color
  $: statusColor = $appState.status.current === 'Balanced' ? 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]' :
                   $appState.status.current === 'Attack' ? 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]' :
                   'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.6)]';
</script>

<svelte:head>
  <title>MIGRU Home & Coherence Pulse</title>
</svelte:head>

<TopAppBar title={`${greeting}, ${$settings.profile.name}`} />

<!-- Main Content Area -->
<div class="w-full max-w-5xl mx-auto px-4 py-6 md:py-12 md:grid md:grid-cols-2 md:gap-12 items-center">
  
  <!-- Left Column: Pulse & Status -->
  <div class="flex flex-col items-center justify-center gap-8 mb-8 md:mb-0">
    <!-- Coherence Pulse (Breathing Island) -->
    <div class="relative w-72 h-72 flex items-center justify-center">
      <div class="absolute inset-0 bg-primary/20 dark:bg-primary/30 rounded-full blur-[80px]"></div>
      <div class="absolute inset-4 bg-primary/40 rounded-full blur-[40px]"></div>
      <div class="relative w-48 h-48 rounded-full bg-gradient-to-b from-[#3a7e93] to-primary shadow-[inset_0_2px_20px_rgba(255,255,255,0.2),0_20px_40px_rgba(0,0,0,0.4)] flex items-center justify-center z-10 border border-white/5">
        <div class="absolute inset-0 rounded-full bg-gradient-to-tr from-transparent via-white/10 to-transparent opacity-50"></div>
        <div class="w-24 h-24 bg-primary/80 rounded-full blur-xl mix-blend-overlay"></div>
      </div>
    </div>

    <!-- Status & Context -->
    <div class="flex flex-col items-center gap-3 z-10">
      <div class="flex h-10 items-center justify-center gap-x-2 rounded-full bg-white dark:bg-[#2c3335]/80 border border-slate-200 dark:border-white/5 pl-5 pr-5 shadow-sm backdrop-blur-md">
        <div class="w-2 h-2 rounded-full {statusColor}"></div>
        <p class="text-slate-700 dark:text-white text-sm font-semibold leading-normal">Current State: {$appState.status.current}</p>
      </div>
      <p class="text-slate-500 dark:text-lavender-mist text-sm font-medium leading-normal text-center max-w-[240px]">
        Heart Rate Variability is {$appState.status.hrv}. Breathing rhythm synced.
      </p>
    </div>
  </div>

  <!-- Right Column: Actions & Forecast -->
  <div class="flex flex-col gap-6 w-full max-w-md mx-auto md:max-w-none">
    <!-- Quick Actions -->
    <div class="flex gap-4 w-full justify-center">
      <button on:click={() => goto('/log')} class="group flex-1 flex items-center justify-center overflow-hidden rounded-2xl h-14 bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 hover:border-primary/50 transition-all">
        <span class="material-symbols-outlined text-slate-400 group-hover:text-primary dark:text-slate-400 mr-3 text-[20px]">edit_note</span>
        <span class="text-slate-900 dark:text-white text-sm font-bold tracking-wide">Log Attack</span>
      </button>
      <button on:click={() => goto('/active-relief')} class="group flex-1 flex items-center justify-center overflow-hidden rounded-2xl h-14 bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 hover:border-primary/50 transition-all">
        <span class="material-symbols-outlined text-slate-400 group-hover:text-primary dark:text-slate-400 mr-3 text-[20px]">play_circle</span>
        <span class="text-slate-900 dark:text-white text-sm font-bold tracking-wide">Relief Audio</span>
      </button>
    </div>

    <!-- Forecast Card -->
    <div class="w-full">
      <ForecastCard
        icon={$appState.forecast.riskLevel === 'High' ? 'warning' : 'storm'}
        title={`${$appState.forecast.riskLevel} Risk Front`}
        description={`Pressure is ${$appState.forecast.pressureTrend.toLowerCase()}. Humidity at ${$appState.forecast.humidity}%.`}
        onClick={() => goto('/forecast')}
      />
    </div>

    <!-- Voice Waveform Visualizer -->
    <div class="flex flex-col items-center gap-3 mt-4">
      <div class="h-8 flex items-center justify-center gap-[3px] opacity-70">
        {#each Array(15) as _, i}
          <div 
            class="w-1 bg-primary/30 rounded-full"
            style={`height: ${[2,4,6,3,5,2,3,1,2,4,3,5,2,3,1][i % 15]}px`}
          ></div>
        {/each}
      </div>
      <p class="text-xs text-primary/60 dark:text-lavender-mist/50 font-medium tracking-wide uppercase">Listening</p>
    </div>
  </div>
</div>

<!-- Background Decoration -->
<div class="fixed bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-white dark:from-black/40 to-transparent pointer-events-none z-0"></div>

<BottomNav />