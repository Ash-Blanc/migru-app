<script lang="ts">
	import { onMount } from 'svelte';
	import TopAppBar from '$lib/components/TopAppBar.svelte';
	import BottomNav from '$lib/components/BottomNav.svelte';

	let analytics = {
		onboarding: {
			completion_rate: 0,
			status: 'not_started'
		},
		engagement: {
			weekly_voice_checkins: 0,
			total_voice_sessions: 0,
			current_streak: 0,
			longest_streak: 0,
			last_checkin: null as string | null
		},
		health_outcomes: {
			baseline_attack_frequency: null,
			current_attack_frequency: null,
			migraine_reduction_percentage: null,
			achieved_40_percent_reduction: false,
			days_to_40_percent_reduction: null
		},
		nps: {
			score: null
		}
	};

	let loading = true;

	onMount(async () => {
		try {
			const response = await fetch('http://localhost:8000/api/analytics', {
				headers: {
					Authorization: `Bearer ${localStorage.getItem('clerk_token')}`
				}
			});

			if (response.ok) {
				analytics = await response.json();
			}
		} catch (error) {
			console.error('Failed to load analytics:', error);
		} finally {
			loading = false;
		}
	});

	function getKPIStatus(value: number | null, target: number) {
		if (value === null) return 'gray';
		return value >= target ? 'green' : value >= target * 0.7 ? 'yellow' : 'red';
	}
</script>

<svelte:head>
	<title>Analytics - MIGRU</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-900 to-slate-900">
	<TopAppBar />

	<div class="p-6 pb-24 max-w-6xl mx-auto">
		<h1 class="text-3xl font-bold text-white mb-6">📊 Your Progress</h1>

		{#if loading}
			<div class="flex items-center justify-center h-64">
				<div class="animate-spin w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full"></div>
			</div>
		{:else}
			<!-- Key Performance Indicators -->
			<div class="grid md:grid-cols-3 gap-6 mb-8">
				<!-- Weekly Voice Check-ins -->
				<div class="glass-panel p-6 rounded-2xl">
					<div class="flex items-center justify-between mb-4">
						<span class="text-gray-400">Weekly Check-ins</span>
						<span class="text-2xl">🎤</span>
					</div>
					<div class="text-4xl font-bold text-white mb-2">
						{analytics.engagement.weekly_voice_checkins}
					</div>
					<div class="text-sm text-gray-400">
						Target: 5+ per week
					</div>
					<div class="mt-3 h-2 bg-gray-700 rounded-full overflow-hidden">
						<div
							class="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
							style="width: {Math.min(100, (analytics.engagement.weekly_voice_checkins / 5) * 100)}%"
						></div>
					</div>
				</div>

				<!-- Migraine Reduction -->
				<div class="glass-panel p-6 rounded-2xl">
					<div class="flex items-center justify-between mb-4">
						<span class="text-gray-400">Migraine Reduction</span>
						<span class="text-2xl">📉</span>
					</div>
					<div class="text-4xl font-bold text-white mb-2">
						{analytics.health_outcomes.migraine_reduction_percentage !== null
							? `${Math.round(analytics.health_outcomes.migraine_reduction_percentage)}%`
							: 'N/A'}
					</div>
					<div class="text-sm text-gray-400">
						Target: 40% reduction
					</div>
					{#if analytics.health_outcomes.achieved_40_percent_reduction}
						<div class="mt-3 text-sm text-green-400 font-semibold flex items-center gap-2">
							<span>✅</span>
							<span>Goal achieved in {analytics.health_outcomes.days_to_40_percent_reduction} days!</span>
						</div>
					{:else}
						<div class="mt-3 h-2 bg-gray-700 rounded-full overflow-hidden">
							<div
								class="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
								style="width: {Math.min(100, (analytics.health_outcomes.migraine_reduction_percentage || 0) / 40 * 100)}%"
							></div>
						</div>
					{/if}
				</div>

				<!-- Current Streak -->
				<div class="glass-panel p-6 rounded-2xl">
					<div class="flex items-center justify-between mb-4">
						<span class="text-gray-400">Current Streak</span>
						<span class="text-2xl">🔥</span>
					</div>
					<div class="text-4xl font-bold text-white mb-2">
						{analytics.engagement.current_streak}
					</div>
					<div class="text-sm text-gray-400">
						Best: {analytics.engagement.longest_streak} days
					</div>
					<div class="mt-3 text-sm text-purple-400">
						Keep going! Daily check-ins help reduce attacks
					</div>
				</div>
			</div>

			<!-- Detailed Metrics -->
			<div class="grid md:grid-cols-2 gap-6">
				<!-- Engagement Stats -->
				<div class="glass-panel p-6 rounded-2xl">
					<h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
						<span>💬</span>
						<span>Engagement Metrics</span>
					</h2>

					<div class="space-y-4">
						<div>
							<div class="flex justify-between text-sm mb-1">
								<span class="text-gray-400">Total Voice Sessions</span>
								<span class="text-white font-semibold">{analytics.engagement.total_voice_sessions}</span>
							</div>
							<div class="h-2 bg-gray-700 rounded-full overflow-hidden">
								<div
									class="h-full bg-purple-500 transition-all duration-500"
									style="width: {Math.min(100, analytics.engagement.total_voice_sessions)}%"
								></div>
							</div>
						</div>

						<div>
							<div class="flex justify-between text-sm mb-1">
								<span class="text-gray-400">Last Check-in</span>
								<span class="text-white font-semibold">
									{analytics.engagement.last_checkin ? new Date(analytics.engagement.last_checkin).toLocaleDateString() : 'Never'}
								</span>
							</div>
						</div>

						<div>
							<div class="flex justify-between text-sm mb-1">
								<span class="text-gray-400">Onboarding</span>
								<span class="text-white font-semibold">
									{analytics.onboarding.completion_rate}%
								</span>
							</div>
							<div class="h-2 bg-gray-700 rounded-full overflow-hidden">
								<div
									class="h-full bg-green-500 transition-all duration-500"
									style="width: {analytics.onboarding.completion_rate}%"
								></div>
							</div>
						</div>
					</div>
				</div>

				<!-- Health Outcomes -->
				<div class="glass-panel p-6 rounded-2xl">
					<h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
						<span>💊</span>
						<span>Health Outcomes</span>
					</h2>

					<div class="space-y-4">
						<div class="flex justify-between items-center">
							<span class="text-gray-400">Baseline Frequency</span>
							<span class="text-white font-semibold">
								{analytics.health_outcomes.baseline_attack_frequency !== null
									? `${analytics.health_outcomes.baseline_attack_frequency}/month`
									: 'Calculating...'}
							</span>
						</div>

						<div class="flex justify-between items-center">
							<span class="text-gray-400">Current Frequency</span>
							<span class="text-white font-semibold">
								{analytics.health_outcomes.current_attack_frequency !== null
									? `${analytics.health_outcomes.current_attack_frequency}/month`
									: 'Calculating...'}
							</span>
						</div>

						{#if analytics.health_outcomes.baseline_attack_frequency !== null && analytics.health_outcomes.current_attack_frequency !== null}
							<div class="pt-4 border-t border-gray-700">
								<div class="flex items-center gap-2 mb-2">
									<span class="text-2xl">
										{(analytics.health_outcomes.migraine_reduction_percentage ?? 0) > 0 ? '📉' : '📊'}
									</span>
									<span class="text-lg font-semibold text-white">
										{(analytics.health_outcomes.migraine_reduction_percentage ?? 0) > 0 ? 'Improving!' : 'Tracking...'}
									</span>
								</div>
								<p class="text-sm text-gray-400">
									{(analytics.health_outcomes.migraine_reduction_percentage ?? 0) > 0
										? `You've reduced migraine frequency by ${Math.round(analytics.health_outcomes.migraine_reduction_percentage ?? 0)}%`
										: 'Keep tracking to see your progress'}
								</p>
							</div>
						{/if}
					</div>
				</div>
			</div>

			<!-- Insights -->
			<div class="mt-6 glass-panel p-6 rounded-2xl">
				<h2 class="text-xl font-semibold text-white mb-4 flex items-center gap-2">
					<span>💡</span>
					<span>Insights</span>
				</h2>

				<div class="space-y-3">
					{#if analytics.engagement.weekly_voice_checkins >= 5}
						<div class="p-3 bg-green-900/30 rounded-lg border border-green-700">
							<p class="text-green-300 text-sm">
								✅ Great job! You hit your weekly check-in goal. Users with 5+ check-ins see 40% faster improvement.
							</p>
						</div>
					{:else}
						<div class="p-3 bg-yellow-900/30 rounded-lg border border-yellow-700">
							<p class="text-yellow-300 text-sm">
								💪 Try to reach 5 voice check-ins this week for optimal results.
							</p>
						</div>
					{/if}

					{#if (analytics.health_outcomes.migraine_reduction_percentage ?? 0) >= 40}
						<div class="p-3 bg-purple-900/30 rounded-lg border border-purple-700">
							<p class="text-purple-300 text-sm">
								🎉 Amazing! You've achieved the 40% reduction goal. Keep up your routine to maintain these results.
							</p>
						</div>
					{/if}

					{#if analytics.engagement.current_streak >= 7}
						<div class="p-3 bg-blue-900/30 rounded-lg border border-blue-700">
							<p class="text-blue-300 text-sm">
								🔥 You're on a {analytics.engagement.current_streak}-day streak! Consistency is key to migraine management.
							</p>
						</div>
					{/if}
				</div>
			</div>
		{/if}
	</div>

	<BottomNav />
</div>

<style>
	.glass-panel {
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}
</style>
