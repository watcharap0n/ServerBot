<template>
  <div>
    <v-container>
      <v-card>
        <v-toolbar
            color="primary"
            dark
            flat
        >
          <v-icon>mdi-view-dashboard</v-icon>
          <v-toolbar-title>BOT</v-toolbar-title>
        </v-toolbar>
        <v-row
            class="pa-4"
            justify="space-between"
        >
          <v-col cols="5">
            <v-treeview
                :active.sync="active"
                :items="items"
                :load-children="fetchItems"
                :open.sync="open"
                activatable
                color="warning"
                open-on-click
                transition
            >
              <template v-slot:prepend="{ item }">
                <v-icon v-if="!item.children">
                  mdi-account
                </v-icon>
              </template>
            </v-treeview>
          </v-col>

          <v-col
              class="d-flex text-center"
          >
            <v-scroll-y-transition mode="out-in">
              <div
                  v-if="!selected"
                  class="text-h6 grey--text text--lighten-1 font-weight-light"
                  style="align-self: center;"
              >
                Select a Item
              </div>
              <v-card
                  v-else
                  :key="selected.id"
                  class="pt-6 mx-auto"
                  flat
                  max-width="400"
              >
                <v-card-text>

                  {{ selected }}

                </v-card-text>
                <v-divider></v-divider>

              </v-card>
            </v-scroll-y-transition>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </div>
</template>

<script>

import {mapGetters} from "vuex";

export default {
  data: () => ({
    data: [],
    active: [],
    avatar: null,
    open: [],
    users: [],
  }),

  computed: {
    items() {
      return [
        {
          name: 'YourName',
          children: this.users,
        },
      ]
    },
    selected() {
      if (!this.active.length) return undefined
      const id = this.active[0]
      return this.users.find(user => user.id === id)
    },
    ...mapGetters({
      cards: "treeview/getInitialized",
    })
  },

  methods: {
    async fetchItems(item) {
      if (this.item) return

      const path = `/card?access_token=asdf`
      this.$store.commit('treeview/setPath', path)
      await this.$store.dispatch('treeview/initialized')
      item.children.push(...this.cards)

    },
  },
}
</script>

<style scoped>
</style>