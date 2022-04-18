<template>

  <v-card>
    <v-toolbar flat>
      <v-btn
          color="red"
          icon
          @click="close"
      >
        <v-icon>mdi-close</v-icon>


      </v-btn>

      <v-toolbar-title>Data Table</v-toolbar-title>
    </v-toolbar>

    <v-card-text>

      <v-data-table
          :headers="headers"
          :items="transactions"
          :items-per-page="5"
      >

      </v-data-table>

    </v-card-text>

  </v-card>

</template>

<script>
export default {
  props: {
    dialogFullScreen: {
      type: Boolean,
      required: false,
    },
    headers: {
      required: true,
    },
    transactions: {
      required: true
    }
  },

  data() {
    return {}
  },

  methods: {
    close() {
      this.$emit('update:dialogFullScreen', false)
    }
  }
}
</script>

<style>

</style>