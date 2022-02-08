<template>
  <div>
    <v-app style="font-family: 'Ubuntu', sans-serif;" class="bg-gray-200">
      <NaviDraw :router-items="items"/>
      <Bar/>
      <div
          v-if="$auth.loggedIn"
          :style="`margin-left: ${$vuetify.application.left}px; margin-top: ${$vuetify.application.top}`"
          class="bg-gray-100 h-screen"
      >
        <br><br><br>
        <Nuxt @routerHandle="handler($event)"/>
        <Snackbar></Snackbar>
      </div>
    </v-app>
  </div>
</template>

<script>
import Snackbar from "@/components/Snackbar";
import Bar from "../components/app/Bar.vue"
import NaviDraw from "../components/layout/NaviDraw";
import Button from "../components/app/Button";

export default {
  middleware: ['auth-admin'],
  components: {Bar, Button, NaviDraw, Snackbar},
  props: ['toolbarTitle'],
  data() {
    return {
      items: [],
    }
  },
  methods: {
    handler(router) {
      this.items = [
        {title: 'หน้าหลัก', icon: 'mdi-home', url: `/`},
        {title: 'แดชบอร์ด', icon: 'mdi-view-dashboard', url: `/callback/dashboard/${router.channel}`},
        {title: 'สร้างการ์ด', icon: 'mdi-robot-happy', url: `/callback/card/${router.channel}`},
        {title: 'สอนบอท', icon: 'mdi-robot-happy', url: `/callback/intent/${router.channel}`},
        {title: 'สร้างกฏ', icon: 'mdi-robot-happy', url: `/callback/rule/${router.channel}`},
        {title: 'ตอบโดยเร็ว', icon: 'mdi-robot-happy', url: `/callback/button/${router.channel}`},
        {title: 'ตั้งค่า', icon: 'mdi-account-box', url: `/callback/setting/${router.channel}`},
      ]
    }
  }
}

</script>

<style scoped>
</style>