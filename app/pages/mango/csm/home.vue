<template>
  <v-card flat
          color="grey lighten-5"
          class="justify-space-between align-center">
    <v-card-actions>
      <v-btn
          fab
          small
          color="secondary"
          class="text-decoration-none"
          to="/mango/csm"
      >
        <v-icon>mdi-arrow-u-left-top</v-icon>
      </v-btn>
      <v-subheader class="text-h6">เลือกโครงการ</v-subheader>
    </v-card-actions>

    <v-container>
      <v-card flat color="grey lighten-5">
        <v-virtual-scroll
            :items="items"
            :item-height="300"
            class="h-auto"
        >
          <template v-slot:default="{ item }">
            <v-card link class="text-decoration-none" :to="`/mango/csm/form/${item.topic}`">
              <v-img
                  height="160"
                  :src="item.src"
              ></v-img>

              <v-card-title class="justify-center">
                {{ item.topic }}
              </v-card-title>
            </v-card>
          </template>
        </v-virtual-scroll>
      </v-card>
    </v-container>

  </v-card>
</template>

<script>
export default {
  layout: 'public',
  data() {
    return {
      items: [
        {
          'src': 'https://cdn.vuetifyjs.com/images/cards/sunshine.jpg',
          'topic': 'โครงการบ้านร่มเย็น',
          'id': '1',
        },
        {
          'src': 'https://cdn.vuetifyjs.com/images/cards/cooking.png',
          'topic': 'โครงกานบ้านสุขสันต์',
          'id': '2'
        },
        {
          'src': 'https://cdn.vuetifyjs.com/images/cards/house.jpg',
          'topic': 'โครงการเอมฤดี',
          'id': '3'
        },
      ]
    }
  }
}
</script>

<style scoped>
</style>