<template>
  <div>
    <h1>Landing Page</h1>
    <button @click="$router.push('/pageone')">Go to Page One</button>
    <button @click="$router.push('/pagetwo')">Go to Page Two</button>
    <button @click="$router.push('/pagethree')">Go to Page Three</button>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
}
</script>
