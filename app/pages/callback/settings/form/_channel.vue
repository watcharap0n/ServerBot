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
        <v-card flat>

          <v-card-title>
            Custom Form

          </v-card-title>
          <v-divider></v-divider>

          <v-card-text>
            <v-container>
              <Form/>

            </v-container>
          </v-card-text>

        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Settings from "@/components/app/Settings";
import Form from "@/components/settings/Form";

export default {
  components: {
    Settings,
    Form
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