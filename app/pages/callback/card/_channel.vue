<template>
  <div>

  </div>
</template>

<script>
export default {
  data() {
    return {}
  },
  async created() {
    await this.$parent.$emit('routerHandle', this.$route.params);
  }
}
</script>

<style scoped>
</style>