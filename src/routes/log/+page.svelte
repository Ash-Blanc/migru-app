<script lang="ts">
  import { goto } from '$app/navigation';
  import { addLog, updateStatus } from '$lib/stores';

  let severity = 5;
  let selectedSymptoms: string[] = [];
  let notes = '';

  const symptomsList = [
    'Throbbing', 'Nausea', 'Light Sensitivity', 'Sound Sensitivity', 
    'Aura', 'Dizziness', 'Neck Pain', 'Fatigue'
  ];

  function toggleSymptom(symptom: string) {
    if (selectedSymptoms.includes(symptom)) {
      selectedSymptoms = selectedSymptoms.filter(s => s !== symptom);
    } else {
      selectedSymptoms = [...selectedSymptoms, symptom];
    }
  }

  function handleSave() {
    addLog({
      type: 'attack',
      severity,
      symptoms: selectedSymptoms,
      notes
    });
    
    // Automatically update status if severity is high
    if (severity > 3) {
      updateStatus('Attack');
    }

    goto('/');
  }
</script>

<div class="max-w-md mx-auto px-4 py-8 min-h-screen flex flex-col">
  <header class="flex items-center gap-4 mb-8">
    <button on:click={() => history.back()} class="btn btn-circle btn-ghost">
      <span class="material-symbols-outlined">arrow_back</span>
    </button>
    <h1 class="text-2xl font-bold">Log Attack</h1>
  </header>

  <div class="flex-1 space-y-8">
    <!-- Severity Slider -->
    <div class="form-control w-full">
      <label class="label" for="severity-range">
        <span class="label-text font-bold text-lg">Severity (1-10)</span>
        <span class="label-text-alt text-xl font-bold text-primary">{severity}</span>
      </label>
      <input 
        id="severity-range"
        type="range" 
        min="1" 
        max="10" 
        bind:value={severity} 
        class="range range-primary" 
        step="1" 
      />
      <div class="w-full flex justify-between text-xs px-2 mt-2 opacity-50">
        <span>Mild</span>
        <span>Moderate</span>
        <span>Severe</span>
      </div>
    </div>

    <!-- Symptoms -->
    <div>
      <h3 class="font-bold text-lg mb-4">Symptoms</h3>
      <div class="flex flex-wrap gap-2">
        {#each symptomsList as symptom}
          <button 
            class="btn btn-sm rounded-full {selectedSymptoms.includes(symptom) ? 'btn-primary' : 'btn-outline'}"
            on:click={() => toggleSymptom(symptom)}
          >
            {symptom}
            {#if selectedSymptoms.includes(symptom)}
              <span class="material-symbols-outlined text-sm">check</span>
            {/if}
          </button>
        {/each}
      </div>
    </div>

    <!-- Notes -->
    <div class="form-control">
      <label class="label" for="notes">
        <span class="label-text font-bold text-lg">Notes</span>
      </label>
      <textarea 
        id="notes"
        class="textarea textarea-bordered h-24" 
        placeholder="Any triggers or specific details..."
        bind:value={notes}
      ></textarea>
    </div>
  </div>

  <div class="mt-8 pb-8">
    <button class="btn btn-primary w-full btn-lg rounded-2xl shadow-lg" on:click={handleSave}>
      <span class="material-symbols-outlined">save</span>
      Save Log
    </button>
  </div>
</div>