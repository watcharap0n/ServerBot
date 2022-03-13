<template>
  <div>
    <v-card flat
    >
      <v-card-text>
        <v-btn
            color="info"
            block
            dark
        >
          Settings Profile
        </v-btn>
      </v-card-text>

      <v-card-text>
        <v-list>
          <v-list-item-group
              v-model="selected"
              color="info"
          >
            <v-list-item
                link
                class="text-decoration-none"
                dense
                v-for="(v, k) in itemsList"
                :key="k"
                :to="v.router"
            >
              <v-list-item-icon>
                <v-icon>
                  {{ v.icon }}
                </v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  {{ v.title }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selected: 0,
      itemsList: [
        {
          icon: 'mdi-table-large', title: 'DataTable', router: `/callback/setting/datatable/${this.$route.params.channel}`
        },
        {
          icon: 'mdi-inbox', title: 'Inbox', router: `/callback/setting/inbox/${this.$route.params.channel}`
        },
        {
          icon: 'mdi-send-outline', title: 'Send', router: `/callback/setting/send/${this.$route.params.channel}`
        },
        {
          icon: 'mdi-account', title: 'Profile', router: `/callback/setting/profile/${this.$route.params.channel}`
        },
      ]
    }
  }
}
</script>

<style scoped>
</style>