<template>

  <v-card class="text-center p-2">
    <v-card-text>
      <v-switch
          dense
          :color="`${intent.ready ? '#12AE7E': 'red'}`"
          :label="`${intent.ready ? 'เปิดใช้งาน': 'ปิดใช้งาน'}`"
          v-model="intent.ready"
      ></v-switch>
      <div :hidden="!intent.ready">
        <p class="text-xl font-normal font-extrabold text-green-500">สอนบอท</p>
        <v-text-field
            append-outer-icon="mdi-send"
            @click:append-outer="sendQues"
            v-model="question"
            label="คำถาม"
            filled
            @keydown.enter="sendQues"
            clearable
        ></v-text-field>
        <v-combobox
            v-model="intent.question"
            label="คำถามที่สอนไป"
            :items="intent.question"
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
                @click:close="remove(item)"
            >
              <strong>{{ item }}</strong>&nbsp;

            </v-chip>
          </template>
        </v-combobox>


        <p class="text-xl font-normal font-extrabold text-green-500">คำตอบ</p>
        <v-switch
            v-model="intent.status_flex"
            label="Card"
        >
        </v-switch>
        <div v-if="!intent.status_flex">
          <v-text-field
              append-outer-icon="mdi-send"
              @click:append-outer="sendAns"
              v-model="answer"
              label="คำตอบ"
              filled
              @keyup.enter="sendAns"
              clearable
          ></v-text-field>
          <v-combobox
              v-model="intent.answer"
              label="คำตอบทั้งหมด"
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
              v-model="selected"
              :items="modelCard"
              append-outer-icon="mdi-card-bulleted-outline"
              menu-props="auto"
              hide-details
              label="Select"
              single-line
          ></v-select>
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
          color="#12AE7E"
          text
          x-large
      >บันทึกประเภทการตอบ
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
      showReady: true,
      showText: "",
      showFlex: "",
      selected: "",
      showCard: false,
      valid: true,
      question: "",
      answer: "",
      intent: {
        name: "",
        access_token: "",
        ready: true,
        status_flex: false,
        card: "",
        question: [],
        answer: [],
      },
      modelCard: [
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
      if (this.question)
      this.intent.question.push(this.question)
      this.question = ''
    },
    sendAns() {
      if (this.answer)
      this.intent.answer.push(this.answer)
      this.answer = ''
    },
    remove(item) {
      this.intent.question.splice(this.intent.question.indexOf(item), 1)
      this.intent.question = [...this.intent.question]
    },
    removeAns(item) {
      this.intent.answer.splice(this.intent.answer.indexOf(item), 1)
      this.intent.answer = [...this.intent.answer]
    },
  },
}
</script>

<style scoped>
.v-chip {
  overflow: initial;
}
</style>