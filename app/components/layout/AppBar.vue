<template>
  <v-app-bar
      flat
      fixed
      :style="`margin-left: ${$vuetify.application.left}px;`"
  >
    <v-toolbar-title>Platform CHATBOT</v-toolbar-title>

    <v-spacer></v-spacer>

    <Button icon="icon" :have-icon="true" name-icon="mdi-heart" color="pink accent-2"/>
    <Button icon="icon" :have-icon="true" name-icon="mdi-magnify" color="pink accent-2"/>
    <div class="pa-2" v-if="$auth.loggedIn">
      <Button name-btn="ออกจากระบบ" text="text" :btn-submit="logout"/>
    </div>

    <div v-else>
      <Button to="/authentication" text="text" name-btn="เข้าสู่ระบบ"/>
    </div>
  </v-app-bar>
</template>

<script>
import Button from "../app/Button";
export default {
  components: {Button},
  methods:{
    logout() {
      this.$auth.logout()
          .then(() => {
            this.$router.push('/authentication')
          })
    }
  }
}
</script>

<style scoped>
</style>