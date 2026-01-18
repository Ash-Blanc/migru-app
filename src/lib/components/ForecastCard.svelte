<script lang="ts">
  import { riskLevel, hrv } from '$lib/stores';
  import { CloudRain, TrendingDown, Activity } from 'lucide-svelte';
  import { clsx } from 'clsx';
</script>

<div class="card bg-base-100 shadow-xl border border-base-200">
  <div class="card-body p-5">
    <div class="flex justify-between items-start">
      <div>
        <h2 class="card-title text-sm opacity-70 uppercase tracking-wide">Migraine Risk</h2>
        <div class={clsx("text-4xl font-black mt-1", {
            "text-success": $riskLevel === 'Low',
            "text-warning": $riskLevel === 'Moderate',
            "text-error": $riskLevel === 'High'
        })}>
            {$riskLevel}
        </div>
      </div>
      <div class={clsx("p-3 rounded-full bg-opacity-10", {
            "bg-success text-success": $riskLevel === 'Low',
            "bg-warning text-warning": $riskLevel === 'Moderate',
            "bg-error text-error": $riskLevel === 'High'
      })}>
        <TrendingDown size={24} />
      </div>
    </div>

    <div class="divider my-2"></div>

    <div class="grid grid-cols-2 gap-4">
        <!-- Weather/Barometer -->
        <div class="flex items-center gap-3">
            <div class="bg-blue-50 p-2 rounded-lg text-blue-500">
                <CloudRain size={20} />
            </div>
            <div>
                <div class="text-xs opacity-60">Pressure</div>
                <div class="font-semibold text-sm">Falling</div>
            </div>
        </div>

        <!-- HRV -->
        <div class="flex items-center gap-3">
            <div class="bg-purple-50 p-2 rounded-lg text-purple-500">
                <Activity size={20} />
            </div>
            <div>
                <div class="text-xs opacity-60">HRV</div>
                <div class="font-semibold text-sm">{$hrv}ms</div>
            </div>
        </div>
    </div>
  </div>
</div>
