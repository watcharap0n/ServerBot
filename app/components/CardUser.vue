<template>
  <div>
    <v-card flat>
      <v-card-title align="center">
        <v-tabs
            v-model="tab"
            background-color="deep-purple accent-4"
            centered
        >
          <v-tabs-slider></v-tabs-slider>

          <v-tab
              v-for="(v, k) in items"
              :key="k"
          >
            {{ v.header }}
            <v-icon>{{ v.icon }}</v-icon>
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item
              v-for="(v, k) in contents"
              :key="k"
          >
            <v-card>
              <v-card-text>
                {{ v }}
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>


      </v-card-title>

      <v-card-text>

      </v-card-text>

    </v-card>

  </div>
</template>

<script>
export default {
  data() {

    return {
      tab: null,
      items: [
        {'header': 'Sign In', 'icon': 'mdi-login'},
        {'header': 'Sign Up', 'icon': 'mdi-account-plus'}
      ],
      contents: ['user', 'no user']
    }

  },
  methods: {}
}
</script>

<style scoped>
</style>