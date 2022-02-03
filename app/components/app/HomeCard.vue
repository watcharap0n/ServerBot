<template>
  <v-card
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
        :src="img_path"
    >
      <template v-slot:placeholder>
        <v-layout fill-height align-center justify-center ma-0>
          <v-progress-circular indeterminate color="tertiary">
          </v-progress-circular>
        </v-layout>
      </template>
    </v-img>

    <v-card-title>{{ nameChannel }} LINE
      &nbsp;
      <v-icon color="success">mdi-chat</v-icon>
    </v-card-title>

    <v-card-text>
      <v-container class="-m-5">
        <div class="text-base font-bold text-gray-900">รายละเอียดบอท :</div>
        <v-row class="m-2">
          <div class="font-medium text-gray-800">ชื่อ:</div> &nbsp;
          <div>{{ displayName }}</div>
        </v-row>
        <v-row class="m-2">
          <div class="font-medium text-gray-800">ไอดี:</div> &nbsp;
          <div>{{ basicId }}</div>
        </v-row>
        <v-row class="m-2">
          <div class="font-medium text-gray-800">ไอดีผู้ใช้:</div> &nbsp;
          <div>{{ userId }}</div>
        </v-row>
        <v-row class="m-2">
          <div class="font-medium text-gray-800">premium id:</div> &nbsp;
          <div v-if="premium === null">บัญชีธรรมดา</div>
          <div>{{ premium }}</div>
        </v-row>
        <v-row class="m-2">
          <div class="font-medium text-gray-800">แชทโหมด:</div> &nbsp;
          <div>{{ chatMode }}</div>
        </v-row>
      </v-container>

    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn :to="endpoint"
             color="primary"
             text
      >ไปยังช่องทาง
      </v-btn>
      <Dialog name-btn="แก้ไข" color-btn="warning" :dialog="dialogUpdate"
              :card-text="`อัพเดทช่องทาง \n ชื่อ ${nameChannel}`" card-title="อัพเดทช่องทาง"
      />
      <Dialog name-btn="ลบ" color-btn="red" :dialog="dialogDelete"
              :card-text="`ลบช่องทาง \n ชื่อ ${nameChannel}`" card-title="ลบช่องทาง"
      />
    </v-card-actions>
  </v-card>
</template>


<script>
import Dialog from "@/components/app/Dialog";

export default {
  components: {Dialog},
  props: [
    'nameChannel', 'description', 'img_path',
    'displayName', 'basicId', 'premium', 'chatMode',
    'userId', 'endpoint', "dialogDelete", "dialogUpdate",
  ],
  data() {
    return {
    }
  },
  methods: {}
}
</script>