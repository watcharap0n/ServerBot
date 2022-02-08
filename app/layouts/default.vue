<template>
  <div>
    <v-app style="font-family: 'Ubuntu', sans-serif;" class="bg-gray-200">
      <v-app-bar
          flat
          dense
          fixed
          :style="`margin-left: ${$vuetify.application.left}px;`"
      >
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
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
          <span class="leading-snug p-1"
                v-on="on"
                v-bind="on"
          >
            {{ $auth.user.username }}
          </span>
            <v-btn
                icon
                v-on="on"
                v-bind="on"
            >
              <v-avatar>
                <img :src="$auth.user.img_path" alt="src">
              </v-avatar>
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
                <h2>{{ $auth.user.username }}</h2>
                <p class="text-caption mt-1">
                  {{ $auth.user.email }}
                </p>
                <v-divider class="my-3"></v-divider>
                <v-btn
                    color="#12AE7E"
                    block
                    depressed
                    rounded
                    text
                >
                  แก้บัญชี
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
        <h2 class="p-5">Platform CHATBOT</h2>

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
              v-for="item in itemsRouter"
              :key="item.title"
              link
              :to="item.url"
              @click="changePageTitle(item.title)"
          >
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-navigation-drawer>

      <div
          v-if="$auth.loggedIn"
          :style="`margin-left: ${$vuetify.application.left}px; margin-top: ${$vuetify.application.top}`"
          class="bg-gray-100 h-screen"
      >
        <br><br><br>



        <Nuxt @routerHandle="handler($event)"/>
        <Snackbar></Snackbar>
      </div>
    </v-app>
  </div>
</template>

<script>
import Snackbar from "@/components/Snackbar";
import Button from "../components/app/Button";

export default {
  middleware: ['auth-admin'],
  components: {Button, Snackbar},
  data() {
    return {
      nameBar: 'PLATFORM CHATBOT',
      selectedItem: 0,
      drawer: true,
      itemsRouter: [],
      data: [],
      active: [],
      avatar: null,
      open: [],
      users: [],
    }
  },
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
  },
  methods: {
    handler(router) {
      this.itemsRouter = [
        {title: 'หน้าหลัก', icon: 'mdi-home', url: `/`},
        {title: 'แดชบอร์ด', icon: 'mdi-view-dashboard', url: `/callback/dashboard/${router.channel}`},
        {title: 'สร้างการ์ด', icon: 'mdi-robot-happy', url: `/callback/card/${router.channel}`},
        {title: 'สอนบอท', icon: 'mdi-robot-happy', url: `/callback/intent/${router.channel}`},
        {title: 'สร้างกฏ', icon: 'mdi-robot-happy', url: `/callback/rule/${router.channel}`},
        {title: 'ตอบโดยเร็ว', icon: 'mdi-robot-happy', url: `/callback/button/${router.channel}`},
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
    async fetchItems(item) {
      if (this.item) return

      const path = `/card?access_token=asdf`
      return this.$axios.get(path)
          .then((res) => {
            res.data.forEach((v) => {
              v.id = v._id
            })
            console.log(res.data)
            item.children.push(...res.data)
          })
          .catch((err) => {
            console.error(err)
          })
    },
  }
}

</script>

<style scoped>
</style>