<template>
  <div>
    <v-app style="font-family: 'Ubuntu', sans-serif;" class="bg-gray-200">
      <NaviDraw/>
      <AppBar/>
      <div
          v-if="$auth.loggedIn"
          :style="`margin-left: ${$vuetify.application.left}px; margin-top: ${$vuetify.application.top}`"
          class="bg-gray-100 h-screen"
      >
        <br><br><br>
        <Nuxt/>
      </div>
    </v-app>
  </div>
</template>

<script>
import AppBar from "../components/layout/AppBar";
import NaviDraw from "../components/layout/NaviDraw";
import Button from "../components/app/Button";

export default {
  components: {AppBar, Button, NaviDraw},
  props: ['toolbarTitle'],
  data() {
    return {

    }
  },
  methods: {

  }
}

</script>

<style scoped>
</style>