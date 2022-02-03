<template>
  <div>
    <Bar name-title="Platform Chatbot | HOME"/>
    <div class="text-4xl m-16 text-center">
      <h2>เลือกบอทที่ต้องการใช้งาน</h2>
    </div>

    <v-item-group multiple>
      <v-row>
        <v-col
            cols="12"
            sm="4"
            v-for="(v, k) in channels"
            :key="k"
        >
          <v-item>
            <HomeCard
                :endpoint="`/callback/channel/${v.token}`"
                :name-channel="v.name"
                :img_path="v.bot_info.picture_url"
                :basic-id="v.bot_info.basic_id"
                :premium="v.bot_info.premium_id"
                :chat-mode="v.bot_info.chat_mode"
                :display-name="v.bot_info.display_name"
                :user-id="v.bot_info.user_id"
                :dialog-delete="dialogDelete"
                :dialog-update="dialogUpdate"
            />
          </v-item>
        </v-col>
      </v-row>
    </v-item-group>


  </div>
</template>

<script>
import Bar from "~/components/app/Bar";
import HomeCard from "~/components/app/HomeCard";

export default {
  components: {Bar, HomeCard},
  layout: "home",
  data() {
    return {
      channels: [],
      dialogUpdate: false,
      dialogDelete: false,
    }
  },
  async created() {
    const path = '/callback/channel/info'
    await this.$axios.get(path)
        .then((res) => {
          this.channels = res.data
        })
        .catch((err) => {
          console.error(err)
        })
  },
  methods: {
    updateChannel(){

    },
    deleteChannel(){
      // const path = `http://localhost:8500/callback/channel/delete/${}`
    }
  }
}
</script>

<style scoped>
</style>