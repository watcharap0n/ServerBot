<template>
  <div>
    <v-dialog
        v-model="dialog"
        persistent
        max-width="290"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            :color="colorBtn"
            dark
            v-bind="attrs"
            v-on="on"
            text
        >
          {{ nameBtn }}
        </v-btn>
      </template>
      <v-card>
        <v-card-title class="text-h5">
          {{ cardTitle }}
        </v-card-title>
        <v-card-text>
          {{ cardText }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              color="red darken-1"
              text
              @click="dialog = false"
          >
            ยกเลิก
          </v-btn>
          <v-btn
              color="green darken-1"
              text
          >
            ตกลง
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  props: ['dialog', 'nameBtn', 'colorBtn', 'cardTitle',
    'cardText']
}
</script>

<style scoped>
</style>