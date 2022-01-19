<template>
  <div>

    <div v-if="$auth.loggedIn">
      {{ $auth.user }}
    </div>

    <div v-else>
      <NuxtLink to="/authentication">
        <v-btn>SignIn</v-btn>
      </NuxtLink>
    </div>

  </div>
</template>

<script>
export default {}
</script>

<style scoped>
</style>