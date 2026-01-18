<script lang="ts">
  import { fly, scale, fade } from 'svelte/transition';
  import { clsx } from 'clsx';
  import { Activity, Moon, Utensils, Zap, Droplets, Check } from 'lucide-svelte';
  import { logs, userStatus, riskLevel, hrv, showToast } from '$lib/stores';
  import { goto } from '$app/navigation';
  
  let severity = 5;
  let symptoms: string[] = [];
  let triggers: string[] = [];
  let showAllSymptoms = false;
  let notes = '';
  let isSaving = false;
  
  // Symptom options with neutral emojis
  const primarySymptoms = [
    { name: "Nausea", emoji: "🤢" },
    { name: "Aura", emoji: "👁️" },
    { name: "Light sensitivity", emoji: "💡" },
    { name: "Throbbing", emoji: "🔴" }
  ];
  const secondarySymptoms = [
    { name: "Sound sensitivity", emoji: "🔊" },
    { name: "Dizziness", emoji: "🌀" },
    { name: "Neck pain", emoji: "🦴" },
    { name: "Brain fog", emoji: "☁️" }
  ];
  
  // Common triggers
  const commonTriggers = [
    { name: "Poor sleep", icon: Moon },
    { name: "Stress", icon: Zap },
    { name: "Skipped meal", icon: Utensils },
    { name: "Dehydrated", icon: Droplets }
  ];

  function toggleSymptom(s: string) {
    if (symptoms.includes(s)) {
      symptoms = symptoms.filter(i => i !== s);
    } else {
      symptoms = [...symptoms, s];
    }
  }
  
  function toggleTrigger(t: string) {
    if (triggers.includes(t)) {
      triggers = triggers.filter(i => i !== t);
    } else {
      triggers = [...triggers, t];
    }
  }

  async function saveLog() {
    if (isSaving) return;
    isSaving = true;

    // Simulate network delay for better UX
    await new Promise(r => setTimeout(r, 800));

    const newEntry = {
      id: crypto.randomUUID(),
      date: new Date().toISOString(),
      severity,
      symptoms,
      triggers,
      notes
    };

    logs.update(current => [newEntry, ...current]);

    if (severity >= 7) {
      userStatus.set("Attack");
      riskLevel.set("High");
      hrv.update(n => Math.max(20, n - 5));
    } else if (severity >= 4) {
      userStatus.set("Prodromal");
      riskLevel.set("Moderate");
      hrv.update(n => Math.max(30, n - 2));
    } else {
      userStatus.set("Balanced");
      riskLevel.set("Low");
      hrv.update(n => Math.min(100, n + 2));
    }

    showToast("Entry saved. Forecast updated.", "success");
    isSaving = false;
    goto('/');
  }
  
  $: severityLabel = severity <= 2 ? 'Minimal' : severity <= 4 ? 'Mild' : severity <= 6 ? 'Moderate' : severity <= 8 ? 'Severe' : 'Intense';
  $: severityEmoji = severity <= 2 ? '😊' : severity <= 4 ? '😐' : severity <= 6 ? '😣' : severity <= 8 ? '😫' : '😵';
</script>

<!-- Log Page with 48px vertical rhythm -->
<div class="space-y-12 pb-8">
  <!-- Header (Proximity: tight grouping) -->
  <div 
    class="text-center"
    style="padding-top: var(--space-md);"
    in:fly={{ y: 20, duration: 500 }}
  >
    <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary mb-3" 
         style="border-radius: var(--radius-full); font-size: var(--text-tiny); font-weight: var(--weight-medium);">
      <Activity size={12} />
      Quick log
    </div>
    <h1 class="tracking-tight">How's it going?</h1>
  </div>

  <!-- Severity Section (Proximity + White Space) -->
  <div 
    class="relative glass-ethereal"
    style="border-radius: var(--radius-xl); padding: var(--space-2xl) var(--space-lg);"
    in:fly={{ y: 20, duration: 500, delay: 100 }}
  >
    <!-- Background glow -->
    <div class={clsx(
      "absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 rounded-full blur-3xl opacity-30 transition-colors duration-500",
      severity <= 3 ? "bg-[hsl(var(--risk-low))]" : severity <= 6 ? "bg-[hsl(var(--risk-moderate))]" : "bg-[hsl(var(--risk-high))]"
    )}></div>
    
    <div class="relative">
      <!-- Emoji display -->
      <div class="text-center mb-6">
        <div class="text-6xl mb-2 transition-all duration-300" style="filter: drop-shadow(0 4px 12px rgba(0,0,0,0.1));">
          {severityEmoji}
        </div>
        <div class="flex items-center justify-center gap-2">
          <span class={clsx(
            "font-black tabular-nums transition-colors duration-300",
            severity <= 3 ? "text-[hsl(var(--risk-low))]" : severity <= 6 ? "text-[hsl(var(--risk-moderate))]" : "text-[hsl(var(--risk-high))]"
          )} style="font-size: var(--text-h1);">
            {severity}
          </span>
          <span class="opacity-50" style="font-size: var(--text-small);">/10</span>
        </div>
        <p class="font-medium opacity-70 mt-1" style="font-size: var(--text-small);">{severityLabel}</p>
      </div>
      
      <!-- Slider -->
      <div class="px-2">
        <input 
          type="range" 
          min="0" 
          max="10" 
          bind:value={severity} 
          class="range range-primary w-full h-3 rounded-full" 
          step="1" 
        />
        <div class="flex justify-between text-lg mt-2 px-1">
          <span>😊</span>
          <span>😐</span>
          <span>😫</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Symptoms Group (Proximity: 12px internal, 48px external) -->
  <div in:fly={{ y: 20, duration: 500, delay: 200 }}>
    <h3 class="flex items-center gap-2" style="margin-bottom: var(--space-md);">
      <Activity size={14} class="text-primary" />
      Symptoms
    </h3>
    
    <div class="flex flex-wrap gap-2 mb-2">
      {#each primarySymptoms as symptom, i}
        <button 
          class={clsx(
            "btn transition-all duration-300 border-2 gap-2",
            symptoms.includes(symptom.name) 
              ? "btn-primary border-primary shadow-lg shadow-primary/20" 
              : "btn-ghost border-base-300 hover:border-primary/30"
          )}
          style="border-radius: var(--radius-full); min-height: 2.75rem; padding-left: var(--space-md); padding-right: var(--space-md);"
          on:click={() => toggleSymptom(symptom.name)}
          in:scale={{ duration: 200, delay: i * 30 }}
        >
          <span>{symptom.emoji}</span>
          {symptom.name}
        </button>
      {/each}
    </div>
    
    {#if showAllSymptoms}
      <div class="flex flex-wrap gap-2 mb-2" in:fly={{ y: 10, duration: 200 }}>
        {#each secondarySymptoms as symptom}
          <button 
            class={clsx(
              "btn btn-sm transition-all duration-300 border-2 gap-1",
              symptoms.includes(symptom.name) 
                ? "btn-primary border-primary" 
                : "btn-ghost border-base-300"
            )}
            style="border-radius: var(--radius-full);"
            on:click={() => toggleSymptom(symptom.name)}
          >
            <span>{symptom.emoji}</span>
            {symptom.name}
          </button>
        {/each}
      </div>
    {/if}
    
    <button 
      class="text-primary font-medium opacity-70 hover:opacity-100 transition-opacity"
      style="font-size: var(--text-tiny);"
      on:click={() => showAllSymptoms = !showAllSymptoms}
    >
      {showAllSymptoms ? '− Fewer' : '+ More'}
    </button>
  </div>

  <!-- Triggers Group -->
  <div in:fly={{ y: 20, duration: 500, delay: 300 }}>
    <h3 class="flex items-center gap-2" style="margin-bottom: var(--space-md);">
      <Zap size={14} class="text-warning" />
      Possible triggers
    </h3>
    
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
      {#each commonTriggers as trigger, i}
        <button 
          class={clsx(
            "flex items-center gap-3 border-2 transition-all duration-300",
            triggers.includes(trigger.name) 
              ? "border-warning bg-warning/10" 
              : "border-base-300 hover:border-warning/30 bg-base-100/50"
          )}
          style="padding: var(--space-md); border-radius: var(--radius-lg);"
          on:click={() => toggleTrigger(trigger.name)}
          in:scale={{ duration: 200, delay: i * 50 }}
        >
          <svelte:component this={trigger.icon} size={18} class={triggers.includes(trigger.name) ? "text-warning" : "opacity-50"} />
          <span class="font-medium" style="font-size: var(--text-small);">{trigger.name}</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Notes -->
  <div in:fly={{ y: 20, duration: 500, delay: 400 }}>
    <textarea 
      bind:value={notes}
      class="textarea w-full h-20 bg-base-100/30 backdrop-blur-sm border-base-300/50 focus:border-primary/50 focus:ring-2 focus:ring-primary/20 resize-none transition-all duration-300" 
      style="border-radius: var(--radius-lg); font-size: var(--text-body); line-height: 1.625;"
      placeholder="Notes (optional)"
    ></textarea>
  </div>

  <!-- Save Button (Contrast: elevated style) -->
  <div in:fly={{ y: 20, duration: 500, delay: 500 }}>
    <button 
      class={clsx(
        "btn btn-primary w-full font-semibold shadow-2xl shadow-primary/40 hover:shadow-primary/50 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 gap-2 ring-2 ring-primary/20",
        isSaving && "loading opacity-80"
      )}
      style="height: 3.5rem; border-radius: var(--radius-lg); font-size: var(--text-body);"
      on:click={saveLog}
      disabled={isSaving}
    >
      {#if !isSaving}
        <Check size={18} />
      {/if}
      {isSaving ? 'Saving...' : 'Save Entry'}
    </button>
    <p class="text-center opacity-40 mt-3" style="font-size: var(--text-tiny);">
      Logs help track patterns over time
    </p>
  </div>
</div>
