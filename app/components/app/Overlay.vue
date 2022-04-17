<template>
  <v-overlay :value="overlay">

    <div class="text-center">
      <v-progress-circular
          :color="color"
          indeterminate
          size="64"
      ></v-progress-circular>
      <v-subheader>{{ showText }}</v-subheader>

      <v-btn
          :hidden="!showRefresh"
          color="red" class="m-12"
          @click="$router.go();"
      >
        try again
      </v-btn>
    </div>

  </v-overlay>
</template>

<script>
export default {
  props: {
    overlay: {
      required: true
    },
    color: {
      required: false,
      type: String,
      default: 'white',
    },
    showText: {
      required: false,
      type: String,
      default: ''
    },
    showRefresh: {
      required: false,
      default: false,
    }
  }
}
</script>