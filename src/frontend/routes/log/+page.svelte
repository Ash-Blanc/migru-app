<script lang="ts">
  import { fade } from 'svelte/transition';
  
  let severity = 5;
  let symptoms = [];
  const allSymptoms = ["Nausea", "Aura", "Light Sensitivity", "Sound Sensitivity", "Dizziness", "Throbbing"];

  function toggleSymptom(s: string) {
    if (symptoms.includes(s)) {
      symptoms = symptoms.filter(i => i !== s);
    } else {
      symptoms = [...symptoms, s];
    }
  }

  function saveLog() {
    // In a real app, post to backend
    alert("Log saved! (Mock)");
  }
</script>

<div class="space-y-6" in:fade>
  <h1 class="text-2xl font-bold">Log an Event</h1>

  <!-- Severity Slider -->
  <div class="card bg-base-100 border border-base-200 p-4">
    <label class="label">
        <span class="label-text font-bold">Pain Severity</span>
        <span class="label-text-alt text-xl font-bold text-primary">{severity}</span>
    </label>
    <input type="range" min="0" max="10" bind:value={severity} class="range range-primary range-sm" step="1" />
    <div class="w-full flex justify-between text-xs px-2 mt-2 opacity-50">
        <span>None</span>
        <span>Mild</span>
        <span>Severe</span>
        <span>Extreme</span>
    </div>
  </div>

  <!-- Symptoms -->
  <div>
    <h3 class="font-bold mb-3">Symptoms</h3>
    <div class="flex flex-wrap gap-2">
        {#each allSymptoms as symptom}
            <button 
                class="btn btn-sm rounded-full {symptoms.includes(symptom) ? 'btn-primary' : 'btn-outline border-base-300'}"
                on:click={() => toggleSymptom(symptom)}
            >
                {symptom}
            </button>
        {/each}
    </div>
  </div>

  <!-- Notes -->
  <textarea class="textarea textarea-bordered w-full h-24" placeholder="Add notes (e.g., missed meal, stress)..."></textarea>

  <button class="btn btn-primary w-full shadow-lg" on:click={saveLog}>
    Save Entry
  </button>
</div>
