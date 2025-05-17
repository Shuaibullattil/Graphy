<template>
  <div>
    <h2>This is Page Three</h2>
    <button @click="$router.push('/pageone')">Go to Page One</button>
    <button @click="$router.push('/pagetwo')">Go to Page Two</button>
    <button @click="$router.push('/pagethree')">Go to Page Three</button>
  </div>
</template>
