<template>
  <div>
    <div v-if="$auth.loggedIn">
      {{ $auth.user }}
    </div>

    <div v-else>
      <v-btn to="/authentication">SignIn</v-btn>
    </div>
    <h2>Hello bot</h2>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
</style>