<template>
  <div>
    <v-row no-gutters>
      <v-col sm="7">
        <v-img :contain="true"
               height="1080"
               src="https://cdn.vuetifyjs.com/images/parallax/material.jpg">
          <template v-slot:placeholder>
            <v-layout fill-height align-center justify-center ma-0>
              <v-progress-circular indeterminate color="tertiary">
              </v-progress-circular>
            </v-layout>
          </template>
        </v-img>
      </v-col>


      <v-col sm="5">
        <v-container>
          <v-card class="text-center
            overflow-hidden mx-auto" flat>
            <v-tabs
                dark
                centered
                v-model="tab"
                background-color="teal accent-4"
                class="text-center justify-center"
            >
              <v-tabs-slider></v-tabs-slider>
              <v-tab
                  class="text-center justify-center"
                  v-for="(v, k) in items"
                  :key="k"
              >
                {{ v.header }}
                <v-icon>{{ v.icon }}</v-icon>
              </v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item>
                <v-card>
                  <v-card-text>
                    <Login/>
                  </v-card-text>
                </v-card>
              </v-tab-item>


              <v-tab-item>
                <v-card>
                  <v-card-text>
                    <Register/>
                  </v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </v-card>

        </v-container>
      </v-col>

    </v-row>
  </div>
</template>

<script>
import Login from '../components/Login'
import Register from '../components/Register'

export default {
  layout: "empty",
  components: {Login, Register},
  data() {
    return {
      mounted: false,
      title: 'Platform CHATBOT',
      tab: null,
      items: [
        {'header': 'Sign In', 'icon': 'mdi-login'},
        {'header': 'Sign Up', 'icon': 'mdi-account-plus'}
      ],
    }
  },
  mounted() {
    this.mounted = true
    window.addEventListener('resize', this.wrapperHeight)
    this.wrapperHeight()
  },
  methods: {
    wrapperHeight() {
      if (this.mounted) return
      return this.containerHeight
    }
  }

}
</script>

<style scoped>
</style>