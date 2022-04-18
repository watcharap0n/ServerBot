<template>
  <v-sheet
      v-if="loading"
      :color="`grey ${theme.isDark ? 'darken-2' : 'lighten-4'}`"
      class="pa-3"
  >
    <v-row>
      <v-col cols="12"
             sm="4"
             v-for="n in numbers"
             :key="n"
      >
        <v-skeleton-loader
            :loading="loading"
            class="mx-auto"
            max-width="390"
            :type="type"
        ></v-skeleton-loader>
      </v-col>
    </v-row>
  </v-sheet>
</template>


<script>
export default {
  props: {
    loading: {
      required: true,
      type: Boolean,
      default: false
    },
    numbers: {
      default: 9,
      required: true,
      type: Number,
    },
    type: {
      default: 'card-avatar, article, actions',
      required: false,
      type: String
    }
  },
  inject: {
    theme: {
      default: {isDark: false},
    },
  },
}
</script>