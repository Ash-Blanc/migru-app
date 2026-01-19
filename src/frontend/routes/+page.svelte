<script lang="ts">
  import ForecastCard from '$lib/components/ForecastCard.svelte';
  import { userStatus, riskLevel, logs } from '$lib/stores';
  import { ArrowRight, Calendar, Activity, ClipboardList, Shield, Brain, Sparkles, Loader2 } from 'lucide-svelte';
  import { fly, fade, scale } from 'svelte/transition';
  import { SignInButton, ClerkLoaded, ClerkLoading } from 'svelte-clerk';
  import { page } from '$app/stores';
  
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

<ClerkLoading>
  <div class="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
    <Loader2 class="w-8 h-8 animate-spin text-primary opacity-50" />
    <p class="text-sm font-medium opacity-40">Initializing Migru...</p>
  </div>
</ClerkLoading>

<ClerkLoaded let:auth>
  {#if auth?.userId || $page.data.auth?.userId || $page.data.userId}
    <!-- Dashboard -->
    <div class="space-y-12">
      <div 
        class="relative text-center"
        style="padding-top: var(--space-2xl); padding-bottom: var(--space-xl);"
        in:fly={{ y: 20, duration: 500, delay: 100 }}
      >
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none overflow-hidden">
          <div class="w-72 h-36 rounded-full bg-gradient-to-r from-primary/15 via-secondary/10 to-accent/15 blur-3xl animate-breathe"></div>
        </div>
        
        <div class="relative">
          <div class="text-4xl mb-4" in:scale={{ duration: 400, delay: 200 }}>
            {timeEmoji}
          </div>
          
          <h2 class="mb-2">
            {greeting}, <span class="gradient-text">{$page.data.user?.firstName || 'Friend'}</span>
          </h2>
          
          <div class="inline-flex items-center gap-2 px-3 py- rounded-full bg-base-200/50 backdrop-blur-sm font-medium opacity-60" 
               style="font-size: var(--text-tiny); padding: var(--space-xs) var(--space-sm); border-radius: var(--radius-full); margin-top: var(--space-sm);">
            <Calendar size={12} />
            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}
          </div>
        </div>
      </div>

      <div in:fly={{ y: 20, duration: 500, delay: 200 }}>
        <ForecastCard />
      </div>

      <div 
        class="relative overflow-hidden glass-panel card-interactive"
        style="border-radius: var(--radius-lg); padding: var(--space-lg);"
        in:fly={{ y: 20, duration: 500, delay: 300 }}
      >
        <div class="flex items-start gap-3">
          <div class="text-2xl animate-float">{dailyTip.emoji}</div>
          <div>
            <p class="text-primary uppercase tracking-wider mb-1" style="font-size: var(--text-tiny); font-weight: var(--weight-semibold);">Today's note</p>
            <p class="opacity-80" style="font-size: var(--text-small); line-height: 1.625;">{dailyTip.text}</p>
          </div>
        </div>
      </div>

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
                class="group w-full flex items-center gap-3 glass-panel card-interactive text-left"
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
             <div class="p-6 text-center border-2 border-dashed border-base-content/10 opacity-60" 
                  style="border-radius: var(--radius-lg);">
               <ClipboardList size={24} class="mx-auto mb-2 opacity-50" />
               <p class="font-medium" style="font-size: var(--text-tiny);">No logs yet today</p>
             </div>
          {/if}
        </div>
      </div>

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
  {:else}
    <!-- Landing Page -->
    <div class="landing-page">
      <div class="sr-only">Landing Page Rendering</div>
      <div class="min-h-[80vh] flex flex-col items-center justify-center space-y-16 py-12">
      <div class="text-center space-y-6 max-w-xl mx-auto px-4" in:fly={{ y: 20, duration: 600 }}>
          <div class="relative inline-block mb-4">
               <div class="absolute inset-0 bg-primary/20 blur-3xl rounded-full"></div>
               <img src="/favicon.svg" alt="Migru Logo" class="w-24 h-24 relative z-10 mx-auto" />
          </div>
          
          <h1 class="text-4xl sm:text-5xl font-bold leading-tight tracking-tight">
              Predict. Prevent. <br/>
              <span class="gradient-text">Find Relief.</span>
          </h1>
          
          <p class="text-lg text-base-content/60 leading-relaxed max-w-md mx-auto">
              Your personal AI companion for tracking migraine patterns, forecasting risks, and finding active relief when you need it most.
          </p>

          <div class="pt-4">
              <SignInButton mode="modal" forcedRedirectUrl="/">
                  <button class="btn btn-primary btn-lg rounded-full shadow-lg shadow-primary/25 hover:shadow-primary/40 px-8 gap-2 group">
                      Get Started
                      <ArrowRight size={20} class="group-hover:translate-x-1 transition-transform" />
                  </button>
              </SignInButton>
          </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-4xl px-4" in:fly={{ y: 30, duration: 600, delay: 200 }}>
          <div class="glass-panel p-6 rounded-2xl text-center space-y-3">
              <div class="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-500 flex items-center justify-center mx-auto mb-2">
                  <Brain size={24} />
              </div>
              <h3 class="font-semibold text-lg">AI Forecast</h3>
              <p class="text-sm text-base-content/60">Predict migraine risks based on weather, sleep, and your personal triggers.</p>
          </div>

          <div class="glass-panel p-6 rounded-2xl text-center space-y-3">
              <div class="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-500 flex items-center justify-center mx-auto mb-2">
                  <Sparkles size={24} />
              </div>
              <h3 class="font-semibold text-lg">Voice Companion</h3>
              <p class="text-sm text-base-content/60">Talk to your compassionate AI agent for immediate relief guidance and logging.</p>
          </div>

          <div class="glass-panel p-6 rounded-2xl text-center space-y-3">
              <div class="w-12 h-12 rounded-xl bg-green-500/10 text-green-500 flex items-center justify-center mx-auto mb-2">
                  <Shield size={24} />
              </div>
              <h3 class="font-semibold text-lg">Smart Insights</h3>
              <p class="text-sm text-base-content/60">Identify patterns and get personalized tips to keep you feeling your best.</p>
          </div>
      </div>
    </div>
  {/if}
</ClerkLoaded>