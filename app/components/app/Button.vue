<template>

  <v-btn
      :icon="icon"
      class="mx-2"
      :fab="fab"
      :dark="dark"
      :color="color"
      :small="small"
      :text="text"
      :to="to"
  >
    <v-icon dark v-if="haveIcon">
      {{ nameIcon }}
    </v-icon>
    {{ nameBtn }}

  </v-btn>

</template>

<script>
export default {
  props: [
    'to',
    'text',
    'nameBtn',
    'btnSubmit',
    'fab',
    'dark',
    'haveIcon',
    'color',
    'icon',
    'nameIcon',
    'size',
    'small'
  ]
}
</script>

<style scoped>
</style>