<template>
  <div>
    
    <v-row>
      <v-col sm="12"
             cols="12"
      >
        <Header/>
      </v-col>
      <v-col sm="6"
             cols="12"
      >
        <BodyLeft/>
      </v-col>

      <v-col sm="6"
             cols="12"
      >
        <BodyRight/>
      </v-col>
    </v-row>

  </div>
</template>

<script>
import Header from "@/components/charts/dashboard/Header";
import BodyLeft from "@/components/charts/dashboard/BodyLeft";
import BodyRight from "@/components/charts/dashboard/BodyRight";

export default {
  components: {
    Header,
    BodyLeft,
    BodyRight
  },

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