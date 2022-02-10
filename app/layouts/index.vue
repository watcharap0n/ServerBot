<template>
  <div>

    <v-app style="font-family: 'Kanit', sans-serif;">
      <div v-if="$auth.loggedIn">
        <Nuxt/>
        <Snackbar></Snackbar>
      </div>

    </v-app>

  </div>
</template>

<script>
import Snackbar from "@/components/Snackbar";

export default {
  components: {Snackbar},
  middleware: ['auth-admin'],
}
</script>

<style scoped>
</style>