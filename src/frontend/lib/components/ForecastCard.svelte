<script lang="ts">
  import { riskLevel, hrv } from '$lib/stores';
  import { CloudRain, Activity, Smile, Meh, Frown } from 'lucide-svelte';
  import { clsx } from 'clsx';
  import { scale, fade } from 'svelte/transition';
  
  // Practical messages based on risk level
  $: friendlyMessage = {
    'Low': "Clear skies ahead",
    'Moderate': "Stay aware, stay prepared",
    'High': "Take it slow today"
  }[$riskLevel] || "Checking conditions...";
  
  $: tipMessage = {
    'Low': "Good time to get things done",
    'Moderate': "Watch for early warning signs",
    'High': "Rest and hydrate"
  }[$riskLevel] || "";
  
  // Risk-specific colors using new design tokens
  $: riskColorClass = {
    'Low': 'text-[hsl(var(--risk-low))]',
    'Moderate': 'text-[hsl(var(--risk-moderate))]',
    'High': 'text-[hsl(var(--risk-high))]'
  }[$riskLevel] || '';
  
  $: orbGradient = {
    'Low': 'from-[hsl(var(--risk-low))] to-emerald-400',
    'Moderate': 'from-[hsl(var(--risk-moderate))] to-orange-400',
    'High': 'from-[hsl(var(--risk-high))] to-rose-500'
  }[$riskLevel] || '';
  
  $: auraColor = {
    'Low': 'bg-[hsl(var(--risk-low))]',
    'Moderate': 'bg-[hsl(var(--risk-moderate))]',
    'High': 'bg-[hsl(var(--risk-high))]'
  }[$riskLevel] || '';
</script>

<!-- Forecast Card with UI Laws Refinements -->
<div 
  class="relative overflow-hidden"
  style="border-radius: var(--radius-xl);"
  in:scale={{ duration: 400, start: 0.95 }}
>
  <!-- Soft ethereal background -->
  <div class="absolute inset-0 glass-ethereal"></div>
  
  <!-- Backdrop Glow (Ambient) -->
  <div class="absolute inset-0 flex items-center justify-center pointer-events-none overflow-hidden">
    <div class={clsx(
      "w-full h-full opacity-10 transition-colors duration-1000",
      {
        "bg-gradient-to-br from-[hsl(var(--risk-low))]/40 via-transparent to-accent/30": $riskLevel === 'Low',
        "bg-gradient-to-br from-[hsl(var(--risk-moderate))]/40 via-transparent to-orange-300/30": $riskLevel === 'Moderate',
        "bg-gradient-to-br from-[hsl(var(--risk-high))]/40 via-transparent to-rose-300/30": $riskLevel === 'High'
      }
    )}></div>
  </div>
  
  <!-- Content with 48px vertical spacing (UI Laws: White Space) -->
  <div class="relative" style="padding: var(--space-2xl) var(--space-xl);">
    <!-- Focal point with Rule of Thirds positioning -->
    <div class="flex flex-col items-center text-center" style="margin-bottom: var(--space-2xl);">
      
      <!-- Orb with face (Increased size for emphasis - Contrast Law) -->
      <div class="relative mb-8 mt-2">
        <!-- Aura Blob (Closure: incomplete boundary) -->
        <div class={clsx(
          "absolute inset-0 rounded-full blur-3xl opacity-40 animate-pulse-soft transition-colors duration-700 orb-aura",
          auraColor
        )}></div>
        
        <!-- Main orb (Symmetry: perfect circle) -->
        <div class={clsx(
          "relative w-36 h-36 sm:w-40 sm:h-40 rounded-full flex items-center justify-center transition-all duration-700 orb-glow",
          "bg-gradient-to-br",
          orbGradient
        )}>
           <!-- Subtle inner highlight for depth -->
           <div class="absolute inset-0 rounded-full bg-gradient-to-t from-black/10 to-white/20"></div>
           
           <!-- Face Icon (Increased size - Typography Hierarchy) -->
           <div class="relative z-10 transition-transform duration-500 hover:scale-110">
            {#if $riskLevel === 'Low'}
              <Smile size={64} class="text-white drop-shadow-md" strokeWidth={2} />
            {:else if $riskLevel === 'Moderate'}
              <Meh size={64} class="text-white drop-shadow-md" strokeWidth={2} />
            {:else}
              <Frown size={64} class="text-white drop-shadow-md" strokeWidth={2} />
            {/if}
           </div>
        </div>
      </div>
      
      <!-- Risk label (Enhanced Typography) -->
      <div class="flex items-center gap-2" style="margin-bottom: var(--space-md);">
        <h2 class={clsx(
          "transition-colors duration-500",
          riskColorClass
        )} style="font-size: var(--text-h1); font-weight: var(--weight-bold); line-height: 1.2;">
          {$riskLevel} Risk
        </h2>
      </div>
      
      <!-- Message (Improved readability with line-height) -->
      <p class="font-medium opacity-90" style="font-size: var(--text-body); line-height: 1.625; margin-bottom: var(--space-sm);" in:fade={{ duration: 300 }}>
        {friendlyMessage}
      </p>
      
      <!-- Tip box (Proximity: grouped with message) -->
      <div class="px-4 py-2 border border-base-content/5 inline-block font-medium opacity-70" 
           style="border-radius: var(--radius-md); background-color: rgba(var(--base-100), 0.4); font-size: var(--text-small); margin-top: var(--space-sm);">
         {tipMessage}
      </div>
    </div>
    
    <!-- Metrics (Continuity: horizontal flow, separated by divider) -->
    <div class="relative" style="margin-top: var(--space-2xl); padding-top: var(--space-lg);">
      <div class="absolute inset-x-0 top-0 h-px bg-base-content/5"></div>
      
      <div class="flex gap-3 flex-wrap justify-center">
        <div class="flex items-center gap-2 px-4 py-2.5 bg-base-100/50 backdrop-blur-sm border border-base-content/5" 
             style="border-radius: var(--radius-full);">
          <CloudRain size={16} class="text-blue-400" />
          <span style="font-size: var(--text-small); font-weight: var(--weight-medium);">Pressure dropping</span>
        </div>
        <div class="flex items-center gap-2 px-4 py-2.5 bg-base-100/50 backdrop-blur-sm border border-base-content/5" 
             style="border-radius: var(--radius-full);">
          <Activity size={16} class="text-purple-400" />
          <span style="font-size: var(--text-small); font-weight: var(--weight-medium);">HRV {$hrv}ms</span>
        </div>
      </div>
    </div>
  </div>
</div>
