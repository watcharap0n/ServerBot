<template>
  <div>
    <Bar name-title="Platform Chatbot | HOME"/>
    <div class="text-4xl m-16 text-center">
      <h2>เลือกบอทที่ต้องการใช้งาน</h2>
    </div>

    <v-item-group multiple>
      <v-row>
        <v-col
            v-if="channels.length > 1"
            cols="12"
            sm="4"
            v-for="(v, k) in channels"
            :key="k"
        >
          <v-item>
            <v-card
                v-if="v.token"
                color="#D7F9FA"
                class="mx-auto my-12"
                max-width="390"
                link
            >
              <template slot="progress">
                <v-progress-linear
                    color="deep-purple"
                    height="10"
                    indeterminate
                ></v-progress-linear>
              </template>

              <v-img
                  height="250"
                  :src="v.bot_info.picture_url"
              >
                <template v-slot:placeholder>
                  <v-layout fill-height align-center justify-center ma-0>
                    <v-progress-circular indeterminate color="tertiary">
                    </v-progress-circular>
                  </v-layout>
                </template>
              </v-img>

              <v-card-title>{{ v.name }} LINE
                &nbsp;
                <v-icon color="success">mdi-chat</v-icon>
              </v-card-title>

              <v-card-text>
                <v-container class="-m-5">
                  <div class="text-base font-bold text-gray-900">รายละเอียดบอท :</div>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">ชื่อ:</div> &nbsp;
                    <div>{{ v.bot_info.display_name }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">ไอดี:</div> &nbsp;
                    <div>{{ v.bot_info.basic_id }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">ไอดีผู้ใช้:</div> &nbsp;
                    <div>{{ v.bot_info.user_id }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">premium id:</div> &nbsp;
                    <div v-if="v.bot_info.premium === null">บัญชีธรรมดา</div>
                    <div>{{ v.bot_info.premium }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">แชทโหมด:</div> &nbsp;
                    <div>{{ v.bot_info.chat_mode }}</div>
                  </v-row>
                  <v-row class="m-2">
                    <div class="font-medium text-gray-800">endpoint:</div> &nbsp;
                    <div @click="copyEndpoint(v.url)">
                      คัดลอก
                      <v-icon>
                        mdi-content-copy
                      </v-icon>
                    </div>
                  </v-row>
                </v-container>

              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn :to="`/callback/channel/${v.token}`"
                       color="primary"
                       text
                       class="text-decoration-none"
                >ไปยังช่องทาง
                </v-btn>

                <v-btn color="warning"
                       text
                       @click="updateChannel(v)"
                >แก้ไข
                </v-btn>

                <v-btn color="red"
                       text
                       @click="deleteChannel(v)"
                >ลบ
                </v-btn>
              </v-card-actions>
            </v-card>
            <CreateChannel v-else/>
          </v-item>
        </v-col>


        <v-col
            v-else-if="channels.length === 1"
            cols="12"
            sm="12"
        >
          <CreateChannel/>
        </v-col>
      </v-row>

    </v-item-group>

    <Dialog :dialog.sync="dialogDelete"
            header="ลบข้อมูล"
            body="คุณแน่ใจที่จะลบข้อมูล"
            :submit-dialog="saveD"
            :loading-dialog.sync="btnSpin"
    />

    <Dialog :dialog.sync="dialogUpdate"
            :element-forms.sync="elements"
            header="แก้ไขข้อมูล"
            max-width="500"
            :submit-dialog="save"
            :loading-dialog.sync="btnSpin"
    />
  </div>
</template>

<script>
import Dialog from "@/components/app/Dialog";
import Bar from "~/components/app/Bar";
import CreateChannel from "@/components/app/CreateChannel";

export default {
  components: {Bar, Dialog, CreateChannel},
  layout: 'index',
  data() {
    return {
      btnSpin: false,
      channels: [],
      defaultChannel: {
        token: '',
        name: '',
        access_token: '',
        secret_token: '',
        uid: '',
        date: '',
        time: '',
        url: '',
        bot_info: {}
      },
      name: '',
      token: '',
      access_token: '',
      secret_token: '',
      dialogUpdate: false,
      dialogDelete: false,
      editedIndex: -1,
      elements: [
        {
          color: 'primary',
          label: 'ชื่อช่องทาง',
          rules: [v => !!v || 'กรุณากรอกข้อมูล'],
          value: this.name
        },
        {
          color: 'primary',
          label: 'Access Token',
          rules: [v => !!v || 'กรุณากรอกข้อมูล'],
          value: this.access_token
        },
        {
          color: 'primary',
          label: 'Secret Token',
          rules: [v => !!v || 'กรุณากรอกข้อมูล'],
          value: this.secret_token
        },
      ],
    }
  },
  async created() {
    const path = '/callback/channel/info'
    await this.$axios.get(path)
        .then((res) => {
          this.channels = res.data
          this.channels.unshift(this.defaultChannel)
        })
        .catch((err) => {
          console.error(err)
        })
  },
  methods: {
    updateChannel(item) {
      this.elements[0].value = item.name
      this.elements[1].value = item.access_token
      this.elements[2].value = item.secret_token
      this.dialogUpdate = true
      this.token = item.token
    },
    async save() {
      this.btnSpin = true
      let payload = {
        name: this.elements[0].value,
        access_token: this.elements[1].value,
        secret_token: this.elements[2].value
      }
      const path = `/callback/channel/update/${this.token}`;
      await this.$axios.put(path, payload)
          .then(() => {
            const pathInfo = '/callback/channel/info'
            this.$axios.get(pathInfo)
                .then((res) => {
                  this.channels = res.data
                  this.channels.unshift(this.defaultChannel)
                })
            this.dialogUpdate = false
          })
          .catch((err) => {
            console.error(err);
          })
      this.btnSpin = false
    },
    deleteChannel(item) {
      this.dialogDelete = true
      this.editedIndex = this.channels.indexOf(item)
    },
    async saveD() {
      this.btnSpin = true
      let token = this.channels[this.editedIndex].token
      const path = `/callback/channel/delete/${token}`
      this.$axios.delete(path)
          .then((res) => {
            console.log(res.data)
            this.channels.splice(this.editedIndex, 1)
          })
          .catch((err) => {
            console.error(err)
          })
      this.btnSpin = false
      this.dialogDelete = false
    },
    copyEndpoint(url) {
      this.$copyText(url)
          .then(() => {
            this.$notifier.showMessage({
              content: 'คัดลอก URL แล้ว สามารถนำไปวางยัง Webhook ของคุณได้ที่ LINE',
              color: 'info'
            })
          })
    }
  }
}
</script>

<style scoped>
</style>