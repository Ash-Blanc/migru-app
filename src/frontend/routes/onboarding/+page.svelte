<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let step = 0;
	let onboardingComplete = false;

	const steps = [
		{ title: 'Welcome', component: 'welcome' },
		{ title: 'Voice Baseline', component: 'voice-baseline' },
		{ title: 'Migraine History', component: 'migraine-history' },
		{ title: 'Tone Preference', component: 'tone-preference' }
	];

	onMount(async () => {
		// Check if already completed
		const response = await fetch('/api/onboarding/status', {
			headers: {
				Authorization: `Bearer ${localStorage.getItem('clerk_token')}`
			}
		});

		if (response.ok) {
			const data = await response.json();
			if (data.completed) {
				goto('/');
			}
		}
	});

	function nextStep() {
		if (step < steps.length - 1) {
			step++;
		} else {
			completeOnboarding();
		}
	}

	function prevStep() {
		if (step > 0) {
			step--;
		}
	}

	async function completeOnboarding() {
		const response = await fetch('/api/onboarding/complete', {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${localStorage.getItem('clerk_token')}`
			}
		});

		if (response.ok) {
			onboardingComplete = true;
			setTimeout(() => goto('/'), 2000);
		}
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-900 to-slate-900 p-6">
	<!-- Progress Bar -->
	<div class="max-w-2xl mx-auto mb-8">
		<div class="flex items-center justify-between mb-4">
			{#each steps as stepItem, i}
				<div class="flex flex-col items-center flex-1">
					<div
						class="w-10 h-10 rounded-full flex items-center justify-center mb-2 transition-all duration-300"
						class:bg-purple-500={i <= step}
						class:text-white={i <= step}
						class:bg-gray-700={i > step}
						class:text-gray-400={i > step}
					>
						{i + 1}
					</div>
					<span class="text-xs text-gray-400 text-center">{stepItem.title}</span>
				</div>
				{#if i < steps.length - 1}
					<div
						class="flex-1 h-1 mx-2 mb-8 rounded transition-all duration-300"
						class:bg-purple-500={i < step}
						class:bg-gray-700={i >= step}
					/>
				{/if}
			{/each}
		</div>
	</div>

	<!-- Step Content -->
	<div class="max-w-2xl mx-auto glass-panel p-8 rounded-3xl">
		{#if !onboardingComplete}
			{#if step === 0}
				<!-- Welcome Step -->
				<div class="text-center">
					<h1 class="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
						Welcome to MIGRU 👋
					</h1>
					<p class="text-lg text-gray-300 mb-6">
						Your voice-first AI companion for migraine management
					</p>
					<div class="text-left space-y-4 mb-8">
						<div class="flex items-start gap-3">
							<span class="text-2xl">🎤</span>
							<div>
								<h3 class="font-semibold text-white">Voice-First Experience</h3>
								<p class="text-gray-400">Talk naturally to track your health and get support</p>
							</div>
						</div>
						<div class="flex items-start gap-3">
							<span class="text-2xl">🧠</span>
							<div>
								<h3 class="font-semibold text-white">AI Pattern Recognition</h3>
								<p class="text-gray-400">Predicts attacks 48 hours in advance</p>
							</div>
						</div>
						<div class="flex items-start gap-3">
							<span class="text-2xl">🌊</span>
							<div>
								<h3 class="font-semibold text-white">Breathing & Relief Tools</h3>
								<p class="text-gray-400">Evidence-based interventions when you need them</p>
							</div>
						</div>
						<div class="flex items-start gap-3">
							<span class="text-2xl">📊</span>
							<div>
								<h3 class="font-semibold text-white">Track Your Progress</h3>
								<p class="text-gray-400">See real reduction in attack frequency</p>
							</div>
						</div>
					</div>
					<p class="text-sm text-gray-400 mb-6">
						This onboarding takes about 2 minutes. Let's get started!
					</p>
				</div>
			{:else if step === 1}
				<!-- Voice Baseline Step -->
				<div>
					<h2 class="text-3xl font-bold mb-4 text-white">Voice Baseline</h2>
					<p class="text-gray-300 mb-6">
						We'll capture a 30-second voice sample to establish your baseline vocal characteristics.
						This helps us detect stress and prodromal indicators later.
					</p>

					<div class="bg-purple-900/30 rounded-xl p-6 mb-6">
						<h3 class="font-semibold text-white mb-3">Instructions:</h3>
						<ol class="space-y-2 text-gray-300">
							<li>1. Find a quiet space</li>
							<li>2. Click "Start Recording"</li>
							<li>3. Talk naturally about your day for 30 seconds</li>
							<li>4. Speak in your normal, relaxed voice</li>
						</ol>
					</div>

					<div class="text-center">
						<div class="mb-4">
							<div class="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center animate-pulse">
								<span class="text-5xl">🎤</span>
							</div>
						</div>
						<button
							class="btn btn-primary btn-lg"
							on:click={() => {
								// TODO: Implement voice recording
								alert('Voice baseline recording will be implemented with Web Audio API');
							}}
						>
							Start Recording
						</button>
					</div>
				</div>
			{:else if step === 2}
				<!-- Migraine History Step -->
				<div>
					<h2 class="text-3xl font-bold mb-4 text-white">Migraine History</h2>
					<p class="text-gray-300 mb-6">
						Help us understand your migraine patterns better
					</p>

					<div class="space-y-4">
						<div>
							<label class="block text-sm font-medium text-gray-300 mb-2">
								How often do you experience migraines?
							</label>
							<select class="select select-bordered w-full">
								<option>Rarely (less than 1/month)</option>
								<option>Occasionally (1-3/month)</option>
								<option>Frequently (4-8/month)</option>
								<option>Chronic (15+ days/month)</option>
							</select>
						</div>

						<div>
							<label class="block text-sm font-medium text-gray-300 mb-2">
								Common triggers (select all that apply)
							</label>
							<div class="grid grid-cols-2 gap-2">
								{#each ['Stress', 'Poor sleep', 'Dehydration', 'Skipped meals', 'Bright lights', 'Weather changes', 'Caffeine', 'Alcohol'] as trigger}
									<label class="flex items-center gap-2 cursor-pointer">
										<input type="checkbox" class="checkbox checkbox-primary" />
										<span class="text-gray-300">{trigger}</span>
									</label>
								{/each}
							</div>
						</div>

						<div>
							<label class="block text-sm font-medium text-gray-300 mb-2">
								Most common symptoms (select all that apply)
							</label>
							<div class="grid grid-cols-2 gap-2">
								{#each ['Throbbing pain', 'Nausea', 'Light sensitivity', 'Sound sensitivity', 'Aura', 'Brain fog', 'Neck pain', 'Dizziness'] as symptom}
									<label class="flex items-center gap-2 cursor-pointer">
										<input type="checkbox" class="checkbox checkbox-primary" />
										<span class="text-gray-300">{symptom}</span>
									</label>
								{/each}
							</div>
						</div>
					</div>
				</div>
			{:else if step === 3}
				<!-- Tone Preference Step -->
				<div>
					<h2 class="text-3xl font-bold mb-4 text-white">Choose Your Vibe</h2>
					<p class="text-gray-300 mb-6">
						How would you like the AI to communicate with you?
					</p>

					<div class="grid gap-4">
						<button class="glass-panel p-6 rounded-xl text-left hover:bg-purple-500/20 transition-all">
							<div class="flex items-start gap-4">
								<span class="text-3xl">🌊</span>
								<div>
									<h3 class="font-semibold text-white mb-2">Calm & Soothing</h3>
									<p class="text-gray-400">
										Gentle, measured pace. Like talking to a mindfulness instructor.
									</p>
								</div>
							</div>
						</button>

						<button class="glass-panel p-6 rounded-xl text-left hover:bg-purple-500/20 transition-all">
							<div class="flex items-start gap-4">
								<span class="text-3xl">⚡</span>
								<div>
									<h3 class="font-semibold text-white mb-2">Energetic & Upbeat</h3>
									<p class="text-gray-400">
										Warm and encouraging. Like chatting with a supportive friend.
									</p>
								</div>
							</div>
						</button>

						<button class="glass-panel p-6 rounded-xl text-left hover:bg-purple-500/20 transition-all">
							<div class="flex items-start gap-4">
								<span class="text-3xl">📊</span>
								<div>
									<h3 class="font-semibold text-white mb-2">Neutral & Clinical</h3>
									<p class="text-gray-400">
										Professional and straightforward. Facts over feelings.
									</p>
								</div>
							</div>
						</button>
					</div>

					<div class="mt-6 p-4 bg-blue-900/30 rounded-xl">
						<p class="text-sm text-gray-300">
							💡 Don't worry, you can change this anytime in Settings
						</p>
					</div>
				</div>
			{/if}

			<!-- Navigation Buttons -->
			<div class="flex justify-between mt-8">
				<button
					class="btn btn-ghost"
					disabled={step === 0}
					on:click={prevStep}
				>
					← Back
				</button>
				<button
					class="btn btn-primary"
					on:click={nextStep}
				>
					{step === steps.length - 1 ? 'Complete' : 'Next'} →
				</button>
			</div>
		{:else}
			<!-- Completion Message -->
			<div class="text-center py-12">
				<div class="text-6xl mb-4">🎉</div>
				<h2 class="text-3xl font-bold text-white mb-4">You're all set!</h2>
				<p class="text-gray-300 mb-6">
					Redirecting you to your dashboard...
				</p>
				<div class="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full mx-auto"></div>
			</div>
		{/if}
	</div>
</div>

<style>
	.glass-panel {
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}
</style>
