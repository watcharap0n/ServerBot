<template>
  <div>
    <div v-if="$auth.loggedIn">



    </div>

    <div v-else>
      <v-btn to="/authentication">SignIn</v-btn>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return{

    }
  },
  async created() {
    await this.$parent.$emit('routerHandle', this.$route.params);
  }
}
</script>

<style scoped>
</style>