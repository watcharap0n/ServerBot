<template>
  <div>
    <v-row>
      <v-col
          sm="3"
          cols="12"
      >
        <Settings/>
      </v-col>

      <v-col
          sm="9"
          cols="12">
        <v-card
            flat>

          <v-card-title>
            Custom Form
          </v-card-title>
          <v-divider></v-divider>

          <v-card-text>
            <v-container>

              Here

            </v-container>
          </v-card-text>

        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Settings from "@/components/app/Settings";

export default {
  components: {
    Settings,
  },
  data() {
    return {
      spin: false,
    }
  },
  async created() {
    await this.$parent.$emit('routerHandle', this.$route.params);

  },
  methods: {
    selectItem() {

    },
  }
}
</script>

<style scoped>
</style>