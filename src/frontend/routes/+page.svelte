<script lang="ts">
  import ForecastCard from '$lib/components/ForecastCard.svelte';
  import { userStatus, riskLevel, logs } from '$lib/stores';
  import { ArrowRight, Calendar, Activity, ClipboardList } from 'lucide-svelte';
  import { fly, fade, scale } from 'svelte/transition';
  
  // Dynamic greeting based on time
  const hour = new Date().getHours();
  const greeting = hour < 5 ? "Still up?" : hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : hour < 21 ? 'Good evening' : "Winding down?";
  const timeEmoji = hour < 6 ? '🌙' : hour < 12 ? '☀️' : hour < 17 ? '🌤️' : hour < 21 ? '🌅' : '🌙';
  
  // Reactive Insights based on Logs
  $: recentLogs = $logs.slice(0, 2);
  $: hasLogs = $logs.length > 0;

  // Practical tips based on risk
  $: dailyTip = {
    'Low': { emoji: '✓', text: "Good conditions today. Stick to your routine." },
    'Moderate': { emoji: '📋', text: "Stay hydrated and watch for early signs." },
    'High': { emoji: '⚠️', text: "Consider taking it slow and staying prepared." }
  }[$riskLevel] || { emoji: '→', text: "One step at a time." };
</script>

<!-- Home with 48px vertical rhythm (UI Laws: White Space) -->
<div class="space-y-12">
  <!-- Greeting (Symmetry: centered) -->
  <div 
    class="relative text-center"
    style="padding-top: var(--space-2xl); padding-bottom: var(--space-xl);"
    in:fly={{ y: 20, duration: 500, delay: 100 }}
  >
    <!-- Soft aura glow -->
    <div class="absolute inset-0 flex items-center justify-center pointer-events-none overflow-hidden">
      <div class="w-72 h-36 rounded-full bg-gradient-to-r from-primary/15 via-secondary/10 to-accent/15 blur-3xl animate-breathe"></div>
    </div>
    
    <div class="relative">
      <!-- Time-based emoji -->
      <div class="text-4xl mb-4" in:scale={{ duration: 400, delay: 200 }}>
        {timeEmoji}
      </div>
      
      <!-- Greeting (H2 instead of oversized text) -->
      <h2 class="mb-2">
        {greeting}, <span class="gradient-text">Alex</span>
      </h2>
      
      <!-- Date pill (Proximity: grouped with greeting) -->
      <div class="inline-flex items-center gap-2 px-3 py- rounded-full bg-base-200/50 backdrop-blur-sm font-medium opacity-60" 
           style="font-size: var(--text-tiny); padding: var(--space-xs) var(--space-sm); border-radius: var(--radius-full); margin-top: var(--space-sm);">
        <Calendar size={12} />
        {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}
      </div>
    </div>
  </div>

  <!-- Forecast Card (Rule of Thirds: positioned 1/3 from top) -->
  <div in:fly={{ y: 20, duration: 500, delay: 200 }}>
    <ForecastCard />
  </div>

  <!-- Daily Tip Card (White Space: 48px separation) -->
  <div 
    class="relative overflow-hidden glass-ethereal"
    style="border-radius: var(--radius-lg); padding: var(--space-lg);"
    in:fly={{ y: 20, duration: 500, delay: 300 }}
  >
    <div class="flex items-start gap-3">
      <div class="text-2xl">{dailyTip.emoji}</div>
      <div>
        <p class="text-primary uppercase tracking-wider mb-1" style="font-size: var(--text-tiny); font-weight: var(--weight-semibold);">Today's note</p>
        <p class="opacity-80" style="font-size: var(--text-small); line-height: 1.625;">{dailyTip.text}</p>
      </div>
    </div>
  </div>

  <!-- Recent Activity (Proximity: tight grouping within, loose separation between) -->
  <div in:fly={{ y: 20, duration: 500, delay: 400 }}>
    <div class="flex justify-between items-center" style="margin-bottom: var(--space-md);">
      <h3 class="flex items-center gap-2">
        <Activity size={14} class="text-primary" />
        Recent activity
      </h3>
      <a href="/log" class="text-primary flex items-center gap-1 group hover:gap-2 transition-all duration-300" 
         style="font-size: var(--text-tiny);">
        View all 
        <ArrowRight size={12} class="transition-transform duration-300 group-hover:translate-x-0.5" />
      </a>
    </div>

    <div class="space-y-2">
      {#if hasLogs}
        {#each recentLogs as log, i}
          <div 
            class="group w-full flex items-center gap-3 glass-ethereal transition-all duration-300 hover:bg-base-100/20 text-left"
            style="padding: var(--space-md); border-radius: var(--radius-lg);"
            in:fly={{ y: 15, duration: 400, delay: 450 + i * 50 }}
          >
            <div class="text-xl group-hover:scale-110 transition-transform duration-300">
              {log.severity <= 2 ? '😊' : log.severity <= 5 ? '😐' : '😫'}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-center">
                <p class="font-medium group-hover:text-primary transition-colors duration-300" style="font-size: var(--text-small);">
                  {log.severity <= 2 ? 'Feeling okay' : log.severity <= 5 ? 'Mild symptoms' : 'High severity'}
                </p>
                <span class="opacity-40" style="font-size: var(--text-tiny);">{new Date(log.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
              </div>
              <p class="opacity-50 truncate" style="font-size: var(--text-tiny);">
                {log.symptoms.length > 0 ? log.symptoms.join(', ') : 'No symptoms logged'}
              </p>
            </div>
          </div>
        {/each}
      {:else}
        <!-- Empty state -->
         <div class="p-6 text-center border-2 border-dashed border-base-content/10 opacity-60" 
              style="border-radius: var(--radius-lg);">
           <ClipboardList size={24} class="mx-auto mb-2 opacity-50" />
           <p class="font-medium" style="font-size: var(--text-tiny);">No logs yet today</p>
         </div>
      {/if}
    </div>
  </div>

  <!-- Status badge -->
  <div 
    class="text-center pb-8"
    in:fade={{ duration: 400, delay: 500 }}
  >
    <div class="inline-flex items-center gap-2 px-4 py-2 bg-success/10 border border-success/20 text-success" 
         style="border-radius: var(--radius-full);">
      <span class="w-2 h-2 rounded-full bg-success animate-pulse"></span>
      <span style="font-size: var(--text-tiny); font-weight: var(--weight-medium);">{$userStatus} (Live)</span>
    </div>
  </div>
</div>
