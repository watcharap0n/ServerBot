<template>
  <div>
    <v-row>
      <v-col
          sm="3"
          cols="12"
      >
        <Settings/>
      </v-col>

      <v-col
          sm="9"
          cols="12">

        <v-form
            ref="form"
            v-model="valid"
            lazy-validation
        >
          <v-card flat>

            <v-card-title>
              <v-icon
                  color="info"
                  class="p-2"
              >
                mdi-bell-outline
              </v-icon>
              Notifications
            </v-card-title>

            <v-card-text>
              <v-card
                  v-if="botInfo.bot_info"
                  tile
                  flat
                  class="mb-6"
              >
                <v-card
                    class="pa-2 align-self-stretch text-center"
                    flat
                >

                  <v-avatar
                      class="profile"
                      color="grey"
                      size="120"
                      tile
                  >
                    <img
                        v-if="botInfo"
                        :src="botInfo.bot_info.picture_url"
                        @error="setFallbackImageUrl"
                    >
                  </v-avatar>

                </v-card>

                <v-card
                    class="pa-2 align-self-start m-3"
                    flat
                >

                  <div class="text-base font-bold text-gray-900">description :</div>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">name:</div> &nbsp;
                    <div>{{ botInfo.name }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">id line:</div> &nbsp;
                    <div>{{ botInfo.bot_info.basic_id }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">user id:</div> &nbsp;
                    <div>{{ botInfo.bot_info.user_id }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">premium id:</div> &nbsp;
                    <div v-if="botInfo.bot_info.premium === null">บัญชีธรรมดา</div>
                    <div>{{ botInfo.bot_info.premium }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">chat mode:</div> &nbsp;
                    <div>{{ botInfo.bot_info.chat_mode }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">endpoint:</div> &nbsp;
                    <v-btn
                        icon
                        @click="copyEndpoint(botInfo.url)"
                        small
                    >
                      <v-icon color="red">
                        mdi-content-copy
                      </v-icon>
                    </v-btn>
                  </v-row>

                </v-card>
                <v-divider class="mx-4"></v-divider>
                <br>

                <NotifyForm
                    :bot-info="botInfo"
                    :forms="forms"
                    :token="botInfo.token"
                />

              </v-card>
            </v-card-text>

            <v-dialog
                v-model="dialog"
                persistent
                max-width="650px"
            >
              <v-card>
                <v-card-title class="text-h5">
                  <v-icon
                      color="info"
                      class="p-2"
                  >
                    mdi-bell-outline
                  </v-icon>
                  Notification
                </v-card-title>

                <v-card-text>
                  <v-container class=" text-center p-2">

                    <v-text-field
                        v-model="webhook.name"
                        :rules="rules"
                        color="info"
                        label="Name"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="webhook.access_token"
                        :rules="rules"
                        color="info"
                        label="Access token"
                        required
                    ></v-text-field>

                    <v-text-field
                        v-model="webhook.secret_token"
                        :rules="rules"
                        color="info"
                        label="Secret token"
                        required
                    ></v-text-field>

                  </v-container>
                </v-card-text>

                <v-card-actions>

                  <v-spacer></v-spacer>
                  <v-btn
                      :disabled="!valid"
                      class="mr-4"
                      color="red"
                      text
                      @click="cancel"
                  >
                    cancel
                  </v-btn>

                  <v-btn
                      :disabled="!valid"
                      class="mr-4"
                      color="success"
                      text
                      :loading="overlay"
                      @click="save"
                  >
                    Save
                  </v-btn>
                </v-card-actions>

              </v-card>
            </v-dialog>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  color="red"
                  text
                  @click="dialogRemove = true"
              >
                delete
              </v-btn>

              <v-btn
                  color="success"
                  text
              >
                save
              </v-btn>
            </v-card-actions>

            <Dialog
                max-width="400px"
                body="confirm to delete the account channel notifications"
                color-toolbar="red"
                :dialog.sync="dialogRemove"
                header="Confirm to delete"
                :submitDialog="remove"
            />

            <Overlay :overlay="overlay"/>

          </v-card>
        </v-form>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Dialog from "@/components/app/Dialog";
import Settings from "@/components/app/Settings";
import Overlay from "@/components/app/Overlay";
import NotifyForm from "@/components/settings/NotifyForm";

export default {
  components: {
    NotifyForm,
    Settings,
    Dialog,
    Overlay,
  },

  data() {
    return {
      dialogRemove: false,
      botInfo: {},
      forms: [],
      accessToken: '',
      rules: [v => !!v || 'Required'],
      dialog: false,
      overlay: false,
      webhook: {},
      valid: false,
    }
  },

  async created() {
    this.overlay = true
    await this.$parent.$emit('routerHandle', this.$route.params);
    const pathToken = `/callback/channel/info/${this.$route.params.channel}`;
    this.$store.commit('features/setDynamicPath', pathToken);
    await this.$store.dispatch('features/fetchToken');
    this.accessToken = this.$store.getters["features/getToken"];
    await this.getChannel();
    await this.getForm();
    this.overlay = false
  },

  methods: {
    async getChannel() {
      let encoded = encodeURIComponent(this.accessToken);
      const path = `notification/find/webhook?id=${encoded}`;
      await this.$axios.get(path)
          .then((res) => {
            this.botInfo = res.data;
          })
          .catch((err) => {
            console.error(err)
            if (err.response.status === 400) {
              this.dialog = true;
            }
          })
    },

    async getForm() {
      let encoded = encodeURIComponent(this.accessToken);
      const path = `/form/find?access_token=${encoded}`;
      await this.$axios.get(path)
          .then((res) => {
            this.forms = res.data;
            console.log(res.data)
          })
          .catch((err) => {
            console.error(err);
          })
    },

    async save() {
      let form = this.$refs.form.validate();
      if (form) {
        this.overlay = true
        this.webhook.base_access_token = this.accessToken
        const path = '/notification/create/webhook';
        await this.$axios.post(path, this.webhook)
            .then((res) => {
              this.botInfo = res.data;
            })
            .catch((err) => {
              console.error(err);
            })
        this.overlay = false
        this.dialog = false
      }
    },

    cancel() {
      this.$router.push(`/callback/settings/datatable/${this.$route.params.channel}`)
    },

    copyEndpoint(url) {
      this.$copyText(url)
          .then(() => {
            this.$notifier.showMessage({
              content: 'URL is copied, you can paste it to your webhook on LINE.',
              color: 'info'
            })
          })
    },

    setFallbackImageUrl(event) {
      event.target.src = require(`~/assets/images/mango-profile.jpg`)
    },

    async remove() {
      const path = `/notification/delete/webhook/${this.botInfo.token}`;
      await this.$axios.delete(path)
          .then((res) => {
            this.$notifier.showMessage({
              content: `delete to the channel LINE || ${res.status}`,
              color: 'red'
            })
          })
          .catch((err) => {
            console.error(err);
          })
      this.dialogRemove = false;
      await this.$router.push(`/callback/settings/datatable/${this.$route.params.channel}`)

    }
  }
}
</script>

<style scoped>
</style>