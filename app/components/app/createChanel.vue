<template>
  <div>
    <v-container>
      <v-card align="center">
        <v-img

            position="center"
            max-height="400"
            max-width="250"
            :src="require('~/assets/images/mango-profile.jpg')"
            class="center"
        >

        </v-img>
        <v-col sm="8">

          <v-form
              ref="form"
              v-model="valid"
              lazy-validation
          >
            <v-text-field
                :rules="nameRules"
                v-model="name"
                label="์Name"
            ></v-text-field>
            <br>
            <v-text-field
                :rules="accessRules"
                v-model="accessToken"
                label="Access Token"
            >
            </v-text-field>
            <br>
            <v-text-field
                :rules="secretRules"
                v-model="secretToken"
                label="Secret Token"
            >
            </v-text-field>
            <v-text-field
                ref="link"
                :value="link"
                v-model="link"
                label="Link"
                append-icon="mdi-content-copy"
                @click:append="copy('link')"
            >
            </v-text-field>
            <br>
            <br>
            <v-btn
                x-large
                style="width:200px"
                color="#12AE7E"
                rounded
                class="text-white "
                @click="submit"
                :loading="spinSubmit"
                :disabled="!valid"
            >submit
            </v-btn>
            <br>
            <br>
            <br>
            <v-row  justify="center">
              <p>วิธีการติดตั้งและใช้งาน </p>
              <p>Platform CHATBOT</p>
            </v-row>
          </v-form>
        </v-col>
      </v-card>
    </v-container>

  </div>
</template>

<script>

export default {

  data() {
    return {
      copied: false,
      link: "",
      secretToken: "",
      name: "",
      accessToken: "",
      valid: true,
      nameRules: [
        v => !!v || 'กรุณากรอกชื่อ',
      ],
      accessRules: [
        v => !!v || 'กรุณากรอกAccess Token',
      ],
      secretRules: [
        v => !!v || 'กรุณากรอกSecret Token',
      ],
      spinSubmit: false,
    }
  },
  methods: {

    copy(field) {
      const input = this.$refs[field].$refs.input
      input.select()
      document.execCommand('copy')
      input.setSelectionRange(0,0) // unselect
    },
  },

}
</script>

<style scoped>
</style>