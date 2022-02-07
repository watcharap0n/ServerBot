<template>
  <v-navigation-drawer
      app
      permanent
      :style="`margin-top: ${$vuetify.application.top}px`"
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
        color="pink accent-2"
    >
      <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          :to="item.url"
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
</template>

<script>

export default {
  data() {
    return {
      selectedItem: 0,
      items: [
        {title: 'หน้าหลัก', icon: 'mdi-home', url: '/'},
        {title: 'แดชบอร์ด', icon: 'mdi-view-dashboard', url: '/dashboard'},
        {title: 'บอท', icon: 'mdi-robot-happy', url: '/bot'},
        {title: 'ตั้งค่า', icon: 'mdi-account-box', url: '/setting'},
      ],
    }
  }
}
</script>