<template>
  <v-sheet
      v-if="condition"
      :color="`grey ${theme.isDark ? 'darken-2' : 'lighten-4'}`"
      class="pa-3"
  >
    <v-row>
      <v-col cols="12"
             sm="4"
             v-for="n in 9"
             :key="n"
      >
        <v-skeleton-loader
            :loading="condition"
            class="mx-auto"
            max-width="390"
            type="card-avatar, article, actions"
        ></v-skeleton-loader>
      </v-col>
    </v-row>
  </v-sheet>
</template>


<script>
export default {
  props: ['condition'],
  inject: {
    theme: {
      default: {isDark: false},
    },
  },
}
</script>