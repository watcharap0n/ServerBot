<template>
  <v-container class="d-flex justify-center">
    <v-card flat
            class="d-flex flex-column justify-space-between align-center">
      <v-img
          style="margin-top: 100px"
          :src="require('assets/images/mango-profile.jpg')"
          width="157"
          height="72"
      ></v-img>

      <v-subheader class="text-h6">ระบบแจ้งซ่อม</v-subheader>
      <br>
      <br>
      <v-card flat>
        <v-card-text>
          <v-text-field
              prepend-inner-icon="mdi-account-outline"
              small
              rounded
              outlined
              label="เบอร์โทรศัพท์"
          ></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-row>
            <v-col sm="6">
              <v-btn
                  class="text-decoration-none"
                  dark
                  block
                  rounded
                  large
                  color="#00BF9D"
                  to="/mango/csm/home"
              >
                <small>เข้าสู่ระบบ</small>
              </v-btn>
            </v-col>

            <v-col sm="6">
              <v-btn
                  disabled
                  block
                  text
              ></v-btn>
            </v-col>
          </v-row>

        </v-card-actions>

      </v-card>

    </v-card>
  </v-container>
</template>

<script>
import liff from "@line/liff";

export default {
  layout: 'public',

  created() {
    // this.initialized();
  },

  methods: {
    async initialized() {
      await liff.init({liffId: '1655208213-27AWV1L3'},
          () => {
            if (liff.isLoggedIn()) {
              liff.getProfile()
                  .then((profile) => {
                    console.log(profile)
                  })
            } else {
              liff.login();
            }
          });
    }
  },

}
</script>

<style>

</style>