<template>
  <div>

    <v-app style="font-family: 'Kanit', sans-serif;">
      <div v-if="$auth.loggedIn">
        <Nuxt/>
      </div>

    </v-app>

  </div>
</template>

<script>

export default {
  middleware: ['auth-admin'],
}
</script>

<style scoped>
</style>