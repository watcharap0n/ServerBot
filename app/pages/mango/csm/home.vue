<template>
  <v-card flat
          class=" justify-space-between align-center">

    <v-card-title>เลือกโครงการ</v-card-title>

    <v-container>
      <v-card flat>
        <v-virtual-scroll
            :items="items"
            :item-height="300"
            height="560"
        >
          <template v-slot:default="{ item }">
              <v-card link>
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
          'topic': 'โครงการบ้านร่มเย็น'
        },
        {
          'src': 'https://cdn.vuetifyjs.com/images/cards/cooking.png',
          'topic': 'โครงกานบ้านสุขสันต์'
        },
        {
          'src': 'https://cdn.vuetifyjs.com/images/cards/house.jpg',
          'topic': 'โครงการเอมฤดี'
        },
      ]
    }
  }
}
</script>

<style scoped>
</style>