<template>
  <div>
    <v-app :style="cssProps" style="font-family: 'Prompt', sans-serif;" class="bg-gray-100 h-screen">

      <Nuxt/>

      <Overlay
          :overlay="!onLine"
          show-text="Please check your network!"
          :show-refresh="true"
      >
      </Overlay>
    </v-app>

  </div>
</template>

<script>
import Overlay from "@/components/app/Overlay";

export default {

  components: {
    Overlay,
  },

  data() {
    return {
      onLine: navigator.onLine,
      cssProps: {
        backgroundImage: `url(${require('~/assets/images/Bg-login_bot.png')})`
      }

    }
  },

  computed: {
    background() {
      return {
        "background-image": require('~/assets/images/Bg-login_bot.png'),

      }
    }
  }
}
</script>

<style scoped>
</style>