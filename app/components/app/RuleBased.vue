<template>
  <div>
    <v-container>
      <v-col sm="8">
        <v-switch
            v-model="showReady"
            label="Ready"

        >
        </v-switch>
        <div v-if="ruleBased.ready === showReady">

          <v-card>
            <v-card-text class="text-center p-2">
              <v-form ref="formQueCard"
                      v-model="valid">
                <p class="text-xl">สร้างคีย์เวิร์ด</p>
                <v-text-field
                    v-model="ques"
                    label="คีย์เวิร์ด"
                    filled
                    @keydown.enter="sendQues"
                    clearable
                ></v-text-field>
              </v-form>

            </v-card-text>


            <v-card-text class="text-center p-2">
              <p class="text-xl">คำตอบ</p>
              <v-switch
                  v-model="showCard"
                  label="Card"
              >
              </v-switch>
              <div v-if="showCard === false">
                <v-card-text
                    v-model="showText"
                >
                  <v-form ref="formAnsCard"
                          v-model="valid">
                    <v-text-field
                        v-model="ans"
                        label="คำตอบ"
                        filled
                        @keyup.enter="sendAns"
                        clearable
                    ></v-text-field>
                  </v-form>
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

                </v-card-text>
              </div>

              <div v-if="showCard === true">
                <v-card-text
                    v-model="showFlex"
                >
                  <v-select
                      v-model="e2"
                      :items="states"
                      append-outer-icon="mdi-card-bulleted-outline"
                      menu-props="auto"
                      hide-details
                      label="Select"
                      single-line
                  ></v-select>
                </v-card-text>
              </div>
            </v-card-text>
            <v-row justify="end">
              <v-col sm="5">
                <v-btn
                    color="#12AE7E"
                    text
                    x-large
                >บันทึกข้อมูล
                </v-btn>
                <v-btn
                    color="red"
                    fab
                    dark
                    small
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </div>

      </v-col>
    </v-container>


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
      e2: 'Texas',
      showCard: false,
      valid: true,
      ques: "",
      ans: "",
      ruleBased: {
        name: "",
        accessToken: "",
        statusCard: false,
        ready: true,
        idCard: "",
        keyword: "",
        answer: []
      },
      states: [
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
      this.ruleBased.keyword.push(this.ques)
      this.$refs.formQueCard.reset();
      console.log(this.ruleBased.keyword)
    },
    sendAns() {
      this.ruleBased.answer.push(this.ans)
      this.$refs.formAnsCard.reset();
      console.log(this.ruleBased.answer)
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