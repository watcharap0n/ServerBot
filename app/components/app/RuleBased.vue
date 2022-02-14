<template>

  <v-card class="text-center p-2" flat>
    <v-card-text>
      <v-switch
          dense
          :color="`${ruleBased.ready ? '#12AE7E': 'red'}`"
          v-model="ruleBased.ready"
          :label="`${ruleBased.ready ? 'เปิดใช้งาน': 'ปิดใช้งาน'}`"
      >
      </v-switch>
      <div :hidden="!ruleBased.ready">
        <p class="text-xl font-normal font-extrabold text-green-500">สร้างคีย์เวิร์ด</p>
        <v-text-field
            v-model="ruleBased.keyword"
            label="คีย์เวิร์ด"
            filled
            clearable
        ></v-text-field>

        <p class="text-xl font-normal font-extrabold text-green-500">คำตอบ</p>
        <v-switch
            dense
            :color="`${ruleBased.status_flex ? '#12AE7E': 'red'}`"
            v-model="ruleBased.status_flex"
            :label="`${ruleBased.status_flex ? 'เปิดใช้งานตอบแบบการ์ด': 'ปิดใช้งานตอบแบบการ์ด'}`"
        >
        </v-switch>

        <div v-if="!ruleBased.status_flex">
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

        <div v-else>
          <v-select
              v-model="ruleBased.card"
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

</template>

<script>

export default {
  data() {
    return {
      answer: "",
      ruleBased: {
        name: "",
        access_token: "",
        status_flex: false,
        ready: true,
        card: "",
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