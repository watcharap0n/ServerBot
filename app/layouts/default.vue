<template>
  <div>
    <v-app style="font-family: 'Prompt', sans-serif;" class="bg-gray-100 h-screen">
      <v-app-bar
          flat
          dense
          fixed
          :style="`margin-left: ${$vuetify.application.left}px;`"
      >
        <v-btn
            style="margin-right: 20px"
            small
            class="hidden-xs-only "
            @click="drawer = !drawer"
            fab

        >
          <v-icon v-if="drawer">mdi-dots-vertical</v-icon>
          <v-icon v-else>mdi-format-list-bulleted</v-icon>
        </v-btn>

        <v-toolbar-title>{{ nameBar }}</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-bell</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>

        <v-menu
            left
            bottom
        >
          <template v-slot:activator="{ on, attrs }">

            <v-btn
                v-on="on"
                v-bind="on"
                text
                rounded
            >
              <v-icon left>
                mdi-account
              </v-icon>
              {{ $auth.user.username }}
            </v-btn>
          </template>

          <v-card width="300">
            <v-list-item-content
                class="justify-center"
            >
              <div class="mx-auto text-center">
                <v-avatar>
                  <img :src="$auth.user.img_path" alt="src">
                </v-avatar>
                <div class="m-2">
                  <div class="font-semibold">{{ $auth.user.full_name }}</div>
                  <small class="text-caption mt-1">
                    {{ $auth.user.email }}
                  </small>
                </div>
                <v-divider class="my-3"></v-divider>
                <v-btn
                    color="#12AE7E"
                    block
                    depressed
                    rounded
                    text
                >
                  แก้ไขบัญชี
                </v-btn>
                <v-divider class="my-3"></v-divider>
                <v-btn
                    color="red"
                    block
                    depressed
                    rounded
                    text
                    @click="logout"
                >
                  ยกเลิกเชื่อมต่อ
                </v-btn>
              </div>
            </v-list-item-content>
          </v-card>
        </v-menu>
      </v-app-bar>

      <v-navigation-drawer
          app
          v-model="drawer"
      >

        <v-row class="p-2 m-4 text-2xl">
          <div> PLATFORM</div>
          <div class="text-red-600"> CHATBOT</div>
        </v-row>

        <v-divider></v-divider>
        <v-list-item two-line v-if="$auth.loggedIn">
          <v-list-item-avatar>
            <img :src="$auth.user.img_path">
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ $auth.user.username }}</v-list-item-title>
            <v-list-item-subtitle><small>{{ $auth.user.email }}</small></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>
        <v-list-item-group
            v-model="selectedItem"
            color="#12AE7E"
        >
          <v-list-item
              class="text-decoration-none"
              v-for="(item, k) in itemsRouter"
              link
              :key="k"
              :to="item.url"
              @click="changePageTitle(item.title)"
          >
            <v-list-item-icon>
              <v-icon color="red">{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-navigation-drawer>

      <div
          :style="`margin-left: ${$vuetify.application.left}px; margin-top: ${$vuetify.application.top}`"
          class="bg-gray-100 p-20 h-screen"
      >
        <Nuxt @routerHandle="handler"/>
        <Snackbar></Snackbar>
      </div>
    </v-app>
  </div>
</template>

<script>
import Snackbar from "@/components/Snackbar";

export default {
  middleware: ['auth-admin'],
  components: {Snackbar},
  data() {
    return {
      nameBar: 'PLATFORM CHATBOT',
      selectedItem: 0,
      drawer: true,
      itemsRouter: [],
    }
  },
  methods: {
    handler(router) {
      this.itemsRouter = [
        {title: 'หน้าหลัก', icon: 'mdi-home', url: `/`},
        {title: 'แดชบอร์ด', icon: 'mdi-view-dashboard', url: `/callback/dashboard/${router.channel}`},
        {title: 'สร้างการ์ด', icon: 'mdi-cards-outline', url: `/callback/card/${router.channel}`},
        {title: 'สอนบอท', icon: 'mdi-robot-happy', url: `/callback/intent/${router.channel}`},
        {title: 'สร้างกฏ', icon: 'mdi-key-variant', url: `/callback/rule/${router.channel}`},
        {title: 'ตอบโดยเร็ว', icon: 'mdi-reply', url: `/callback/button/${router.channel}`},
        {title: 'ตั้งค่า', icon: 'mdi-account-box', url: `/callback/setting/${router.channel}`},
      ]
    },
    logout() {
      this.$auth.logout()
          .then(() => {
            this.$router.push('/authentication')
          })
    },
    changePageTitle(page) {
      return this.nameBar = page
    },
  }
}

</script>

<style scoped>
</style>