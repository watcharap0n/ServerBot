<template>
  <div>
    <v-row>
      <v-col sm="7">
        <v-parallax height="800" src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"></v-parallax>
      </v-col>


      <v-col sm="5">
        <v-container>
          <Card/>
        </v-container>
      </v-col>

    </v-row>
  </div>
</template>

<script>
import Card from "../components/CardUser";

export default {
  layout: "empty",
  components: {Card},
  data() {
    return {}
  }

}
</script>

<style scoped>
</style>