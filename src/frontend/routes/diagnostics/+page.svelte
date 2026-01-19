<script lang="ts">
  import { onMount } from 'svelte';
  import { apiKeys } from '$lib/stores';
  import { get } from 'svelte/store';

  let checks = {
    secureContext: false,
    mediaDevices: false,
    microphone: 'pending',
    backend: 'pending',
    auth: 'pending',
    socket: 'pending'
  };

  let logs: string[] = [];

  function log(msg: string) {
    logs = [...logs, `${new Date().toLocaleTimeString()} - ${msg}`];
  }

  const getBackendUrl = () => {
    if (typeof window === 'undefined') return 'http://localhost:8000';
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    return `${protocol}//${hostname}:8000`;
  };

  onMount(() => {
    checks.secureContext = window.isSecureContext;
    log(`Secure Context: ${checks.secureContext}`);
    
    if (typeof navigator !== 'undefined' && navigator.mediaDevices) {
        checks.mediaDevices = true;
        log("MediaDevices API available");
    } else {
        log("MediaDevices API MISSING (Browser incompatible or non-secure context)");
    }
  });

  async function testBackend() {
    checks.backend = 'loading';
    try {
        const url = `${getBackendUrl()}/api/status`;
        log(`Fetching ${url}...`);
        const res = await fetch(url);
        if (res.ok) {
            const data = await res.json();
            log(`Backend OK. Status: ${data.status}`);
            checks.backend = 'success';
        } else {
            log(`Backend Error: ${res.status}`);
            checks.backend = 'error';
        }
    } catch (e) {
        log(`Backend Connection Failed: ${(e as Error).message}`);
        checks.backend = 'error';
    }
  }

  async function testAuth() {
    checks.auth = 'loading';
    try {
        const url = `${getBackendUrl()}/hume/auth`;
        log(`Fetching ${url}...`);
        const headers: Record<string, string> = {};
        const key = get(apiKeys.humeKey);
        const secret = get(apiKeys.humeSecret);
        if(key) headers['x-hume-api-key'] = key;
        if(secret) headers['x-hume-secret-key'] = secret;

        const res = await fetch(url, { headers });
        if (res.ok) {
            const data = await res.json();
            if (data.access_token === "mock_token_for_demo_purposes") {
                log("Auth WARNING: Received Mock Token (Keys missing?)");
                checks.auth = 'warning';
            } else {
                log("Auth OK: Received valid token");
                checks.auth = 'success';
            }
        } else {
            log(`Auth Error: ${res.status}`);
            checks.auth = 'error';
        }
    } catch (e) {
        log(`Auth Connection Failed: ${(e as Error).message}`);
        checks.auth = 'error';
    }
  }

  async function testMic() {
    checks.microphone = 'loading';
    try {
        log("Requesting Mic Permission...");
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        log("Mic Permission GRANTED");
        checks.microphone = 'success';
        
        // Stop immediately
        stream.getTracks().forEach(t => t.stop());
    } catch (e) {
        log(`Mic Error: ${(e as Error).message}`);
        checks.microphone = 'error';
    }
  }
</script>

<div class="p-8 max-w-2xl mx-auto space-y-6">
  <h1 class="text-2xl font-bold">Diagnostics</h1>
  
  <div class="card bg-base-100 shadow-xl border border-base-300">
    <div class="card-body">
        <h2 class="card-title">System Checks</h2>
        
        <div class="grid grid-cols-2 gap-4">
            <div class="flex items-center gap-2">
                <span class="badge {checks.secureContext ? 'badge-success' : 'badge-error'}">
                    Secure Context
                </span>
            </div>
             <div class="flex items-center gap-2">
                <span class="badge {checks.mediaDevices ? 'badge-success' : 'badge-error'}">
                    MediaDevices
                </span>
            </div>
        </div>

        <div class="divider"></div>
        
        <div class="flex flex-col gap-2">
            <div class="flex justify-between items-center">
                <span>Backend Connection</span>
                <button class="btn btn-sm" on:click={testBackend}>Test</button>
            </div>
            {#if checks.backend !== 'pending'}
                 <span class="text-xs {checks.backend === 'success' ? 'text-success' : 'text-error'}">
                    {checks.backend.toUpperCase()}
                 </span>
            {/if}

            <div class="flex justify-between items-center">
                <span>Hume Auth</span>
                <button class="btn btn-sm" on:click={testAuth}>Test</button>
            </div>
             {#if checks.auth !== 'pending'}
                 <span class="text-xs {checks.auth === 'success' ? 'text-success' : checks.auth === 'warning' ? 'text-warning' : 'text-error'}">
                    {checks.auth.toUpperCase()}
                 </span>
            {/if}

            <div class="flex justify-between items-center">
                <span>Microphone</span>
                <button class="btn btn-sm" on:click={testMic}>Test</button>
            </div>
             {#if checks.microphone !== 'pending'}
                 <span class="text-xs {checks.microphone === 'success' ? 'text-success' : 'text-error'}">
                    {checks.microphone.toUpperCase()}
                 </span>
            {/if}
        </div>
    </div>
  </div>

  <div class="mockup-code bg-base-300 text-base-content p-4 h-64 overflow-y-auto block">
    <pre><code>{#each logs as log}{log}{'\n'}{/each}</code></pre>
  </div>
</div>
