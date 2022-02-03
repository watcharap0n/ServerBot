<template>
  <div>
    <div v-if="$auth.loggedIn">
      {{ $auth.user }}
    </div>

    <div v-else>
      <v-btn to="/authentication">SignIn</v-btn>
    </div>
    <h2>Hello </h2>
  </div>
</template>

<script>
export default {
  data(){
    return{

    }
  },
  created() {
    console.log(this.$route.params)
  }
}
</script>

<style scoped>
</style>