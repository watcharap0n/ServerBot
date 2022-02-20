<template>
  <div>
    <v-app-bar
        color="#12AE7E"
        dense
        dark
        fixed
        :style="`margin-left: ${$vuetify.application.left}px;`"
    >

      <v-toolbar-title>{{ nameTitle }}</v-toolbar-title>

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
  </div>
</template>

<script>
export default {
  props: ['nameTitle'],
  data() {
    return {}
  },
  methods: {
    logout() {
      this.$auth.logout()
          .then(() => {
            this.$router.push('/authentication')
          })
    }
  }
}

</script>