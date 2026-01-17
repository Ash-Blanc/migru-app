<script lang="ts">
  export let icon: string;
  export let title: string;
  export let description: string;
  export let onClick: () => void = () => {};
</script>

<button 
  class="card card-side bg-base-200 shadow-sm hover:shadow-md transition-all duration-300 w-full mb-4 text-left group"
  on:click={onClick}
>
  <figure class="pl-4 py-4 flex-none">
    <div class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-primary-content transition-colors duration-300">
      <span class="material-symbols-outlined text-2xl">{icon}</span>
    </div>
  </figure>
  <div class="card-body p-4 gap-1">
    <h3 class="card-title text-base font-bold">{title}</h3>
    <p class="text-sm opacity-70 leading-snug">{description}</p>
  </div>
  <div class="pr-4 py-4 flex items-center flex-none">
    <span class="material-symbols-outlined opacity-50 group-hover:translate-x-1 transition-transform">chevron_right</span>
  </div>
</button>