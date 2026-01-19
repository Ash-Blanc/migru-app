<script>
  import { SignIn } from 'svelte-clerk';
</script>

<div class="min-h-[70vh] flex items-center justify-center py-12 px-4">
  <SignIn path="/sign-in" signUpUrl="/sign-up" />
</div>
