<template>

  <v-form class="h-auto">
    <v-card flat
            color="grey lighten-5"
            class="justify-space-between align-center">
      <v-card-actions>
        <v-btn
            fab
            small
            color="secondary"
            class="text-decoration-none"
            to="/mango/helpdesk/home"
        >
          <v-icon>mdi-arrow-u-left-top</v-icon>
        </v-btn>
        <v-subheader class="text-h6">ข้อมูลการติดต่อ</v-subheader>
      </v-card-actions>

      <v-card flat>
        <v-card-text>
          <v-row>
            <v-col cols="12" sm="12">
              <v-text-field
                  v-model="name"
                  outlined
                  rounded
                  placeholder="บริษัท เจริญสิน แอลเลส จำกัด"
                  persistent-hint
                  dense
              ></v-text-field>
            </v-col>
          </v-row>
          <v-subheader style="margin-top: -35px">ชื่อผู้แจ้งซ่อม</v-subheader>

          <v-row style="margin-top: -20px">
            <v-col
                cols="6"
                sm="6"
                style="margin-top: 20px"
            >
            </v-col>
          </v-row>

          <v-row style="margin-top: -40px">
            <v-col cols="7" sm="7">
              <v-text-field
                  outlined
                  rounded
                  label="ระบุชื่อผู้แจ้งซ่อม"
                  persistent-hint
                  dense
              ></v-text-field>
            </v-col>

            <v-col cols="5" sm="5">
              <v-text-field
                  outlined
                  rounded
                  label="เบอร์ติดต่อ"
                  persistent-hint
                  dense
              ></v-text-field>
            </v-col>
          </v-row>

          <v-text-field
              outlined
              rounded
              label="อีเมล"
              persistent-hint
              dense
          ></v-text-field>

          <v-subheader style="margin-top: -20px">รายละเอียดการติดต่อ</v-subheader>

          <v-textarea
              outlined
              rounded
              persistent-hint
              dense
          ></v-textarea>

        </v-card-text>
      </v-card>
      <br>

      <v-card
          flat
          v-for="(item, k) in detailArray"
          :key="k"
      >
        <v-card-actions>
          <div style="margin-left: 20px"> แจ้งเคสหรือปัญหาการใช้งานเกี่ยวกับ {{ k + 1 }}</div>
          <v-spacer></v-spacer>
          <v-btn
              small
              color="red"
              text
              @click="remove(item)"
          >
            ลบ
          </v-btn>
        </v-card-actions>
        <v-card-text>
          <v-row>
            <v-col cols="7">
              <v-select
                  v-model="item.case"
                  label="Error ข้อผิดพลาด"
                  :items="cases"
                  rounded
                  outlined
                  dense
              ></v-select>
            </v-col>

            <v-col cols="5">
              <v-select
                  v-model="item.module"
                  label="Modules"
                  :items="modules"
                  rounded
                  outlined
                  dense
              ></v-select>
            </v-col>
          </v-row>

          <v-text-field
              label="เรื่อง"
              persistent-hint
              dense
              rounded
              outlined
              v-model="item.topic"
          ></v-text-field>

          <v-textarea
              label="รายละเอียด"
              persistent-hint
              dense
              rounded
              outlined
              v-model="item.detail"
          ></v-textarea>

          <v-file-input
              @change="previewImage(item)"
              v-model="item.file"
              placeholder="Remark"
              label="หมายเหตุไฟล์แนบ"
              prepend-icon="mdi-paperclip"
              rounded
              outlined
              dense
              counter
              accept="image/png, image/jpeg"
              :rules="item.rulesImg"
              :show-size="1000"
          >
            <template v-slot:prepend-inner>
              <v-btn
                  small
                  icon
              >
                <v-icon>
                  mdi-camera
                </v-icon>
              </v-btn>
            </template>
            <template v-slot:selection="{ text }">
              <v-chip
                  small
                  label
                  color="primary"
              >
                {{ text }}
              </v-chip>
            </template>
          </v-file-input>

          <img
              v-if="item.file"
              :src="item.url"
          >
        </v-card-text>
      </v-card>

      <v-btn
          text
          color="#00BF9D"
          @click="add"
      >
        <v-icon left>
          mdi-plus
        </v-icon>
        เพิ่มรายละเอียดแจ้งซ่อม
      </v-btn>
      <v-btn
          block
          color="#00BF9D"
          dark
      >
        บันทึก
      </v-btn>

      <div class="text-center">
        <v-snackbar
            color="red"
            v-model="snackbar"
            :timeout="timeout"
        >
          {{ text }}
          <template v-slot:action="{ attrs }">
            <v-btn
                text
                v-bind="attrs"
                @click="snackbar = false"
            >
              Close
            </v-btn>
          </template>
        </v-snackbar>
      </div>
    </v-card>
  </v-form>
</template>

<script>
export default {
  layout: 'public',
  data() {
    return {
      files: null,
      url: null,
      rulesImg: [
        value => !value || value.size < 1000000 || 'image size should be less than 1 MB!',
      ],

      isCameraOpen: false,
      video: null,

      detailArray: [],
      snackbar: false,
      text: 'แจ้งเรื่องสูงสุดได้ 5 เรื่อง',
      timeout: 2000,
      name: '',
      cases: [
        'แบบฟอร์มและรายงาน',
        'Error ข้อผิดพลาดจาการใช้งาน',
        'สอบถามการใช้งาน',
        'Service IT',
        'RE Module',
        'แจ้งเรื่องอื่นๆ'
      ],
      modules: [
        'AP',
        'AR',
        'BD',
        'EVAL',
        'IC',
        'FA',
        'GL',
        'HR',
        'MR',
        'MRP',
        'OF',
        'PO',
        'PM',
        'RE',
        'QCM',
        'RT',
        'SE',
        'CSM',
        'PPN',
        'FN',
        'MAIL',
        'ALL MODULE',
        'Other'
      ]
    }
  },

  created() {
    let item = {
      id: this.detailArray.length + 1,
      case: '',
      module: '',
      topic: '',
      detail: '',
      file: null,
      url: null,
      rulesImg: [
        value => !value || value.size < 1000000 || 'image size should be less than 1 MB!',
      ],
    }
    this.detailArray.push(item)
  },

  computed: {},

  methods: {
    previewImage(item) {
      if (item.file)
        return item.url = URL.createObjectURL(item.file);
    },

    add() {
      let item = {
        id: this.detailArray.length + 1,
        topic: '',
        detail: '',
        file: null,
        url: null,
        rulesImg: [
          value => !value || value.size < 1000000 || 'image size should be less than 1 MB!',
        ],
      }
      if (this.detailArray.length >= 5) {
        this.snackbar = true
      } else {
        this.detailArray.push(item)
      }
    },

    remove(item) {
      this.detailArray.splice(this.detailArray.indexOf(item), 1)
    },

  }


}
</script>

<style scoped>
</style>