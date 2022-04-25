<template>
  <div>

    <v-row>
      <v-col sm="12">
        <v-card flat>
          <v-card-text>
            <DataTable/>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col sm="6">
        <v-card flat>
          <v-card-text>
            <Bar/>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col sm="6">
        <v-card flat>
          <v-card-text>
            <Donut/>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col sm="12">
        <v-card flat>
          <v-card-text>
            <LineChar/>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </div>
</template>

<script>
import LineChar from "@/components/charts/dashboard/LineChar";
import Donut from "@/components/charts/dashboard/Donut";
import Bar from "@/components/charts/dashboard/Bar";
import DataTable from "@/components/charts/dashboard/DataTable";

export default {
  components: {
    LineChar,
    Donut,
    Bar,
    DataTable,
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