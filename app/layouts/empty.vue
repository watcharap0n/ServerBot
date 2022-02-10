<template>
  <div>

    <v-app :style="cssProps">

      <Nuxt/>
    </v-app>

  </div>
</template>

<script>
export default {
  data(){
    return{
      cssProps: {
          backgroundImage: `url(${require('~/assets/images/Bg-login_bot.png')})`
        }

    }
  },
  computed:{
    background(){
      return{
        "background-image": require('~/assets/images/Bg-login_bot.png'),

      }
    }
  }
}
</script>

<style scoped>
</style>