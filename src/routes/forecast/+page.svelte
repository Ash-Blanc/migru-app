<script lang="ts">
  import { goto } from '$app/navigation';
  import { appState } from '$lib/stores';

  // Generate dynamic calendar days
  const today = new Date();
  const days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today);
    d.setDate(today.getDate() - 1 + i); // Start from yesterday
    const isToday = i === 1;
    const isPast = i === 0;
    
    // Simple mock risk logic based on day index
    let type = 'normal';
    if (isPast) type = 'past';
    else if (isToday) type = 'today';
    else if (i === 2 || i === 5) type = 'risk'; // Arbitrary risk days
    else if (i === 3) type = 'safe';

    return {
      day: d.toLocaleDateString('en-US', { weekday: 'short' }),
      date: d.getDate(),
      type
    };
  });
  
  // Reactive factors based on store
  $: factors = [
    { icon: 'wb_sunny', color: 'text-warning', title: 'Barometer', value: $appState.forecast.pressureTrend },
    { icon: 'water_drop', color: 'text-error', title: 'Humidity', value: `${$appState.forecast.humidity}%` },
    { icon: 'bedtime', color: 'text-info', title: 'Sleep', value: '7h 12m' } // Mocked sleep data
  ];
  
  let recommendations = [
    { icon: 'water_full', color: 'info', title: 'Hydrate Now', subtitle: 'Drink 500ml water', checked: false },
    { icon: 'contrast', color: 'warning', title: 'Reduce Light', subtitle: 'Enable dark mode everywhere', checked: false },
    { icon: 'spa', color: 'success', title: 'Magnesium', subtitle: 'Take supplement or soak', checked: false }
  ];
</script>

<div class="bg-base-100 min-h-screen w-full max-w-7xl mx-auto pb-20 md:pb-8">
  <!-- Header -->
  <header class="flex items-center justify-between p-6 pt-8 pb-4">
    <h2 class="text-2xl font-bold">Forecast</h2>
    <button on:click={() => goto('/insights')} class="btn btn-circle btn-ghost">
      <span class="material-symbols-outlined">graphic_eq</span>
    </button>
  </header>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 px-4">
    <!-- Risk Card (Spans 2 cols on desktop) -->
    <section class="md:col-span-2">
      <div class="card bg-base-200 shadow-xl border border-base-300 rounded-[2rem] overflow-hidden h-full">
        <div class="card-body p-6 relative">
          <div class="absolute inset-0 opacity-40 mix-blend-soft-light pointer-events-none">
            <div class="absolute -top-10 -right-10 w-64 h-64 bg-primary rounded-full blur-[80px] animate-breathe"></div>
            <div class="absolute top-20 -left-10 w-48 h-48 bg-secondary rounded-full blur-[60px] opacity-60"></div>
          </div>
          
          <div class="flex justify-between items-start relative z-10">
            <div>
              <div class="badge badge-primary badge-outline gap-2 mb-2">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                </span>
                Live Analysis
              </div>
              <h1 class="text-3xl font-bold">{$appState.forecast.riskLevel} Risk</h1>
            </div>
            <div class="avatar placeholder">
              <div class="bg-gradient-to-tr from-primary to-secondary text-neutral-content rounded-full w-16 h-16 shadow-inner">
                <span class="text-lg font-bold">48h</span>
              </div>
            </div>
          </div>
          
          <p class="text-base-content/70 mt-4 relative z-10">
            Your vocal biomarkers indicate slight fatigue. Barometric pressure is {$appState.forecast.pressureTrend.toLowerCase()} this evening.
          </p>
          <button on:click={() => goto('/assistant')} class="btn btn-sm btn-ghost btn-primary mt-3 relative z-10 w-fit">
            <span class="material-symbols-outlined">mic</span>
            Ask: "What specifically triggered this?"
          </button>
        </div>
      </div>
    </section>

    <!-- Calendar (Spans 1 col) -->
    <section class="md:col-span-1">
      <div class="card bg-base-100 border border-base-200 h-full">
        <div class="card-body p-4">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-lg font-bold">Projected Impact</h3>
            <div class="flex gap-2 text-xs text-base-content/60">
              <span class="flex items-center gap-1"><span class="badge badge-secondary badge-xs"></span> Low</span>
              <span class="flex items-center gap-1"><span class="badge badge-primary badge-xs"></span> High</span>
            </div>
          </div>
          <div class="flex md:grid md:grid-cols-4 md:gap-y-4 gap-2 overflow-x-auto md:overflow-visible no-scrollbar">
            {#each days as day}
              <div class="flex flex-col items-center gap-2 min-w-[3.5rem] {day.type === 'past' ? 'opacity-50' : ''}">
                <span class="text-xs uppercase {day.type === 'today' ? 'font-bold' : 'text-base-content/60'}">
                  {day.day}
                </span>
                <div class={`h-14 w-14 flex items-center justify-center rounded-2xl border relative ${
                  day.type === 'today' ? 'bg-primary border-primary' : 
                  day.type === 'risk' ? 'bg-base-200 border-primary/40' : 
                  'bg-base-200/50 border-transparent text-base-content/60'
                }`}>
                  {day.date}
                  {#if ['today', 'risk', 'safe'].includes(day.type)}
                    <div class={`badge badge-xs absolute bottom-1 ${
                      day.type === 'today' ? 'badge-primary' : 
                      day.type === 'risk' ? 'badge-primary' : 'badge-secondary'
                    }`}></div>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </section>

    <!-- Factors (Full width) -->
    <section class="md:col-span-3">
      <div class="card bg-base-200/50 border border-base-300 rounded-[1.5rem]">
        <div class="card-body p-5">
          <h3 class="card-title text-base">
            <span class="material-symbols-outlined text-primary">insights</span>
            Contributing Factors
          </h3>
          <div class="flex gap-3 overflow-x-auto mt-2 md:grid md:grid-cols-3">
            {#each factors as factor}
              <div class="card card-compact bg-base-300 w-32 shrink-0 md:w-full">
                <div class="card-body items-center text-center">
                  <span class="material-symbols-outlined text-2xl {factor.color}">{factor.icon}</span>
                  <p class="text-[10px] uppercase text-base-content/60 tracking-wide font-bold">{factor.title}</p>
                  <p class="text-sm font-semibold">{factor.value}</p>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
    </section>

    <!-- Recommendations (Grid) -->
    <section class="md:col-span-3 space-y-4">
      <h3 class="text-lg font-bold px-2">Suggested Relief</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        {#each recommendations as rec}
          <div class="card bg-base-200 p-4 rounded-2xl cursor-pointer transition-all hover:bg-base-300">
            <label class="flex items-center justify-between cursor-pointer h-full">
              <div class="flex items-center gap-4">
                <div class={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-${rec.color}/10 text-${rec.color}`}>
                  <span class="material-symbols-outlined">{rec.icon}</span>
                </div>
                <div class="flex flex-col">
                  <span class="font-semibold">{rec.title}</span>
                  <span class="text-sm text-base-content/70">{rec.subtitle}</span>
                </div>
              </div>
              <input type="checkbox" class="checkbox checkbox-{rec.color}" bind:checked={rec.checked} />
            </label>
          </div>
        {/each}
      </div>
    </section>
  </div>
</div>

<!-- Floating Mic Button -->
<div class="fixed bottom-24 right-6 z-50">
  <button on:click={() => goto('/assistant')} class="btn btn-primary btn-circle btn-lg shadow-lg hover:scale-105 transition-transform">
    <span class="material-symbols-outlined text-3xl">mic</span>
  </button>
</div>