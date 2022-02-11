<template>
  <div>

    <v-card class="text-center p-2" flat>
      <v-card-text>
        <v-switch
            dense
            :color="`${showReady ? '#12AE7E': 'red'}`"
            v-model="showReady"
            :label="`${showReady ? 'เปิดใช้งาน': 'ปิดใช้งาน'}`"
        >
        </v-switch>
        <div :hidden="!showReady">
          <p class="text-xl font-normal font-extrabold text-green-500">สร้างคีย์เวิร์ด</p>
          <v-text-field
              v-model="keyword"
              label="คีย์เวิร์ด"
              filled
              @keydown.enter="sendQues"
              clearable
          ></v-text-field>

          <p class="text-xl font-normal font-extrabold text-green-500 m-10">คำตอบ</p>
          <v-switch
              dense
              :color="`${showCard ? '#12AE7E': 'red'}`"
              v-model="showCard"
              :label="`${showCard ? 'เปิดใช้งานตอบแบบการ์ด': 'ปิดใช้งานตอบแบบการ์ด'}`"
          >
          </v-switch>

          <div v-if="!showCard" v-model="showText">
            <v-text-field
                v-model="answer"
                label="คำตอบ"
                filled
                @keyup.enter="sendAns"
                clearable
            ></v-text-field>
            <v-combobox
                v-model="ruleBased.answer"
                label="คำตอบ"
                deletable-chips
                chips
                multiple
                hide-selected
                readonly
            >
              <template v-slot:selection="{ attrs, item, select, selected }">
                <v-chip
                    v-bind="attrs"
                    :input-value="selected"
                    close
                    @click="select"
                    @click:close="removeAns(item)"
                >
                  <strong>{{ item }}</strong>&nbsp;

                </v-chip>
              </template>
            </v-combobox>
          </div>

          <div v-else v-model="showFlex">
            <v-select
                v-model="selected"
                :items="modelCards"
                append-outer-icon="mdi-card-bulleted-outline"
                menu-props="auto"
                hide-details
                label="เลือกการ์ดที่ต้องการใช้งาน"
                single-line
            ></v-select>
          </div>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
         <v-btn
              text
              color="success"
          >
            <v-icon left>mdi-database-plus</v-icon>
            บันทึกข้อมูล
          </v-btn>
          <v-btn
              color="red"
              dark
              text
          >
            <v-icon left>mdi-delete</v-icon>
            ลบข้อมูล
          </v-btn>
      </v-card-actions>
    </v-card>
  </div>


</template>

<script>
import intent from "@/components/app/Intent";

export default {
  data() {
    return {
      showReady: true,
      showText: "",
      showFlex: "",
      selected: '',
      showCard: false,
      valid: true,
      keyword: "",
      answer: "",
      ruleBased: {
        name: "",
        accessToken: "",
        statusCard: false,
        ready: true,
        idCard: "",
        keyword: "",
        answer: []
      },
      modelCards: [
        'Alabama', 'Alaska', 'American Samoa', 'Arizona',
        'Arkansas', 'California', 'Colorado', 'Connecticut',
        'Delaware', 'District of Columbia', 'Federated States of Micronesia',
        'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho',
        'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
        'Louisiana', 'Maine', 'Marshall Islands', 'Maryland',
        'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
        'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
        'North Carolina', 'North Dakota', 'Northern Mariana Islands', 'Ohio',
        'Oklahoma', 'Oregon', 'Palau', 'Pennsylvania', 'Puerto Rico',
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
        'Texas', 'Utah', 'Vermont', 'Virgin Island', 'Virginia',
        'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
      ],

    }
  },
  methods: {
    sendQues() {
      this.ruleBased.keyword.push(this.keyword)
      this.keyword = ''
    },
    sendAns() {
      this.ruleBased.answer.push(this.answer)
    },
    remove(item) {
      this.ruleBased.keyword.splice(this.ruleBased.keyword.indexOf(item), 1)
      this.ruleBased.keyword = [...this.ruleBased.keyword]

    },
    removeAns(item) {
      this.ruleBased.answer.splice(this.ruleBased.answer.indexOf(item), 1)
      this.ruleBased.answer = [...this.ruleBased.answer]
    },
  },
  computed: {},
}
</script>

<style scoped>
.v-chip {
  overflow: initial;
}
</style>