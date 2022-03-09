<template>
  <div>
    <v-app style="font-family: 'Prompt', sans-serif;" class="bg-gray-100 h-auto">
      <v-app-bar
          flat
          fixed
          :style="`margin-left: ${$vuetify.application.left}px;`"
      >
        <v-btn
            style="margin-right: 20px"
            small
            class="hidden-xs-only"
            @click="drawer = !drawer"
            fab
        >
          <v-icon v-if="drawer">mdi-dots-vertical</v-icon>
          <v-icon v-else>mdi-format-list-bulleted</v-icon>
        </v-btn>

        <v-toolbar-title>{{ nameBar }}</v-toolbar-title>


        <v-spacer></v-spacer>

        <v-autocomplete
            class="m-2"
            rounded
            filled
            color="info"
            v-model="model"
            :items="items"
            :loading="isLoading"
            :search-input.sync="search"
            prepend-inner-icon="mdi-magnify"
            clearable
            placeholder="Start typing to Search"
            hide-details
            hide-selected
            item-text="title"
            item-value="url"
        >
          <template v-slot:item="{item}">
            <v-subheader>
              <small>APPS</small>
            </v-subheader>
            <v-list nav>
              <v-list-item-group
                  style="margin-top: -10px"
                  v-model="selectedItem"
                  color="info"
              >
                <v-list-item
                    dense
                    class="text-decoration-none"
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
            </v-list>
          </template>
        </v-autocomplete>

        <v-btn icon>
          <v-icon>mdi-bell</v-icon>
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
                  <img :src="$auth.user.img_path" alt="src"
                       @error="setFallbackImageUrl"
                  >
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

        <div class="p-4">
          <div class="text-xl"> PLATFORM MANGO</div>
          <div class="text-xl text-blue-400"> CHATBOT</div>
          <small class="text-xs text-gray-300">2.1.0</small>
        </div>

        <v-divider></v-divider>

        <v-list-item two-line
                     dense
                     v-if="$auth.loggedIn">
          <v-list-item-avatar>
            <img :src="$auth.user.img_path"
                 @error="setFallbackImageUrl"
            >
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ $auth.user.username }}</v-list-item-title>
            <v-list-item-subtitle><small>{{ $auth.user.email }}</small></v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list nav
                style="margin-top: 10px"
        >
          <v-list-item-group
              v-model="selectedItem"
              color="info"
          >
            <v-list-item
                dense
                class="text-decoration-none"
                v-for="(item, k) in itemsHome"
                link
                :key="k"
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
        </v-list>

        <v-list nav>
          <v-subheader>
            <small>APPS</small>
          </v-subheader>
          <v-list-item-group
              style="margin-top: -10px"
              v-model="selectedItem"
              color="info"
          >
            <v-list-item
                dense
                class="text-decoration-none"
                v-for="(item, k) in itemsApp"
                link
                :key="k"
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
        </v-list>

        <v-list nav>
          <v-subheader>
            <small>Others</small>
          </v-subheader>
          <v-list-item-group
              style="margin-top: -10px"
              v-model="selectedItem"
              color="info"
          >
            <v-list-item
                dense
                class="text-decoration-none"
                v-for="(item, k) in itemsOther"
                link
                :key="k"
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
        </v-list>

      </v-navigation-drawer>

      <div
          :style="`margin-left: ${$vuetify.application.left - 40}px; margin-top: ${$vuetify.application.top}`"
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
      isLoading: false,
      items: [],
      model: null,
      search: null,
      tab: null,

      nameBar: 'PLATFORM CHATBOT',
      selectedItem: 0,
      drawer: true,
      itemsApp: [],
      itemsOther: [],
      itemsHome: []
    }
  },
  watch: {
    model(val) {
      if (val != null) this.tab = 0
      else this.tab = null
    },
    search(val) {
      if (this.items.length > 0) return

      this.isLoading = true

      // Lazily load input items
      this.items = this.itemsApp
      this.isLoading = false
    },
  },
  methods: {
    setFallbackImageUrl(event) {
      event.target.src = require(`~/assets/images/mango-profile.jpg`)
    },
    handler(router) {
      this.itemsApp = [
        {id: 'p1', title: 'Dashboard', icon: 'mdi-view-dashboard-outline', url: `/callback/dashboard/${router.channel}`},
        {id: 'p2', title: 'Flex Message', icon: 'mdi-cards-outline', url: `/callback/card/${router.channel}`},
        {id: 'p3', title: 'Intent', icon: 'mdi-robot-happy-outline', url: `/callback/intent/${router.channel}`},
        {id: 'p4', title: 'Rule Based', icon: 'mdi-dice-5-outline', url: `/callback/rule/${router.channel}`},
        {id: 'p5', title: 'Quick Reply', icon: 'mdi-reply-outline', url: `/callback/button/${router.channel}`},
        {id: 'p6', title: 'Image Map', icon: 'mdi-image-outline', url: `/callback/image/${router.channel}`},
      ]
      this.itemsOther = [
        {title: 'Settings', icon: 'mdi-account-box-outline', url: `/callback/setting/datatable/${router.channel}`},
      ]
      this.itemsHome = [
        {title: 'Home', icon: 'mdi-home-outline', url: `/`},
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