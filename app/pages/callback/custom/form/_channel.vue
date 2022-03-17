<template>
  <div>

  </div>
</template>

<script>

export default {
  data() {
    return {
      spin: false,
    }
  },

  async created() {
    await this.$parent.$emit('routerHandle', this.$route.params);
    await this.getForm();
  },

  methods: {
    async getForm() {
      const path = `/form/find/${this.$route.query.q}`
      await this.$axios.get(path)
          .then((res) => {
            console.log(res.data)
          })
          .catch((err) => {
            console.error(err);
          })
    }
  }
}
</script>

<style scoped>
</style>
