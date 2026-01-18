<script lang="ts">
  import ForecastCard from '$lib/components/ForecastCard.svelte';
  import { userStatus } from '$lib/stores';
  import { ArrowRight, Calendar, Info } from 'lucide-svelte';
</script>

<div class="space-y-6">
  <!-- Greeting -->
  <div>
    <h1 class="text-3xl font-bold">Good Morning, Alex</h1>
    <p class="opacity-60">Here is your daily migraine forecast.</p>
  </div>

  <!-- Forecast Card -->
  <ForecastCard />

  <!-- Status Section -->
  <div class="card bg-base-200 border border-base-300">
    <div class="card-body p-4">
        <h3 class="font-semibold text-sm flex items-center gap-2">
            <Info size={16} />
            Current Status
        </h3>
        <div class="flex items-center justify-between mt-2">
            <span class="badge badge-lg badge-outline">{$userStatus}</span>
            <button class="btn btn-xs btn-ghost text-primary">Update</button>
        </div>
    </div>
  </div>

  <!-- Insights Preview -->
  <div>
    <div class="flex justify-between items-center mb-3">
        <h3 class="font-bold text-lg">Recent Insights</h3>
        <a href="/log" class="text-primary text-sm flex items-center gap-1">
            View Log <ArrowRight size={14} />
        </a>
    </div>

    <div class="space-y-3">
        <!-- Mock Insight Items -->
        <div class="flex items-start gap-3 p-3 bg-base-100 rounded-xl border border-base-200 shadow-sm">
            <div class="bg-orange-100 text-orange-600 p-2 rounded-lg">
                <Calendar size={18} />
            </div>
            <div>
                <p class="text-sm font-medium">Attack Triggered</p>
                <p class="text-xs opacity-60">Yesterday • High Humidity</p>
            </div>
        </div>
    </div>
  </div>
</div>
