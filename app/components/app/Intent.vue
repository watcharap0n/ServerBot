<template>

  <v-card class="text-center p-2" flat>

    <v-card-text>
      <div :hidden="!intent.ready">
        <p class="text-l font-normal ">Intent</p>
        <v-text-field
            rounded
            color="red"
            append-outer-icon="mdi-send"
            @click:append-outer="sendQues"
            v-model="question"
            label="input question"
            filled
            @keydown.enter="sendQues"
            clearable
        ></v-text-field>

        <v-combobox
            v-model="intent.question"
            label="Questions taught"
            :items="intent.question"
            chips
            multiple
            hide-selected
            readonly
        >
          <template v-slot:append-outer>
            <v-btn icon
                   color="info"
                   @click="show = !show"
            >
              <v-icon
                  v-text="`${show ? 'mdi-format-vertical-align-center' : 'mdi-format-line-spacing'}`"
              ></v-icon>
            </v-btn>
          </template>
          <template v-slot:selection="{ attrs, item, select, selected, index }">
            <div v-if="!show">
              <v-chip
                  v-if="index <= 3"
                  dark
                  color="info"
                  v-bind="attrs"
                  :input-value="selected"
                  close
                  @click="select"
                  @click:close="removeQuestion(item)"
              >
                <strong>{{ item }}</strong>&nbsp;
              </v-chip>
              <span v-if="index === 4"
                    class="grey--text text-caption"
              >
                (+{{ intent.question.length - 4 }} others)
              </span>
            </div>
            <div v-else-if="show">
              <v-chip
                  dark
                  color="info"
                  v-bind="attrs"
                  :input-value="selected"
                  close
                  @click="select"
                  @click:close="removeQuestion(item)"
              >
                <strong>{{ item }}</strong>&nbsp;
              </v-chip>
            </div>
          </template>
        </v-combobox>


        <p class="text-l font-normal ">Answer</p>
        <v-switch
            v-model="intent.status_flex"
            label="Enable Flex Message"
            color="info"
        >
        </v-switch>
        <div v-if="!intent.status_flex">
          <v-text-field
              rounded
              color="red"
              append-outer-icon="mdi-send"
              @click:append-outer="sendAns"
              v-model="answer"
              label="input answer"
              filled
              @keyup.enter="sendAns"
              clearable
          ></v-text-field>
          <v-combobox
              v-model="intent.answer"
              label="Answers"
              deletable-chips
              chips
              multiple
              hide-selected
              readonly
          >
            <template v-slot:append-outer>
              <v-btn icon
                     color="info"
                     @click="showAnswer = !showAnswer"
              >
                <v-icon
                    v-text="`${showAnswer ? 'mdi-format-vertical-align-center' : 'mdi-format-line-spacing'}`"
                ></v-icon>
              </v-btn>
            </template>
            <template v-slot:selection="{ attrs, item, select, selected, index }">
              <div v-if="!showAnswer">
                <v-chip
                    v-if="index <= 1"
                    dark
                    color="info"
                    v-bind="attrs"
                    :input-value="selected"
                    close
                    @click="select"
                    @click:close="removeAns(item)"
                >
                  <strong>{{ item }}</strong>&nbsp;
                </v-chip>
                <span v-if="index === 2"
                      class="grey--text text-caption"
                >
                (+{{ intent.answer.length - 2 }} others)
              </span>
              </div>
              <div v-else-if="showAnswer">
                <v-chip
                    dark
                    color="info"
                    v-bind="attrs"
                    :input-value="selected"
                    close
                    @click="select"
                    @click:close="removeAns(item)"
                >
                  <strong>{{ item }}</strong>&nbsp;
                </v-chip>
              </div>
            </template>
          </v-combobox>
        </div>

        <div v-else>
          <v-select
              rounded
              filled
              v-model="intent.card"
              :items="cards"
              item-text="name"
              color="red"
              item-value="_id"
              append-outer-icon="mdi-card-bulleted-outline"
              menu-props="auto"
              item-color="red"
              hide-details
              label="select your flex messages"
              single-line
          ></v-select>
        </div>
      </div>
    </v-card-text>
    <v-card-actions>
      <v-switch
          style="margin-left:5px "
          dense
          color="info"
          :label="`${intent.ready ? 'Enabled': 'Disabled'}`"
          v-model="intent.ready"
      ></v-switch>
      <v-spacer></v-spacer>
      <v-btn
          text
          color="info"
          :loading="!spin"
          @click="todo"
      >
        <v-icon left>mdi-database-plus</v-icon>
        Save
      </v-btn>
      <v-btn
          text
          color="grey"
          dark
          @click="dialog = true"
      >
        <v-icon left>mdi-delete</v-icon>
        Delete
      </v-btn>
    </v-card-actions>

    <Dialog
        :dialog.sync="dialog"
        header="Delete data"
        body="Are you sure to delete the data ?"
        max-width="350"
        :loading-dialog="!spin"
        :submit-dialog="remove"
    >

    </Dialog>
  </v-card>

</template>

<script>
import Dialog from "@/components/app/Dialog";

export default {
  components: {Dialog},
  props: {
    intent: {
      required: false,
      type: Object
    },
    cards: {
      required: false
    },
    users: {
      required: false
    }
  },
  data() {
    return {
      show: false,
      showAnswer: false,
      items: [],
      dialog: false,
      spin: true,
      selected: "",
      showCard: false,
      question: "",
      answer: "",
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
    removeQuestion(item) {
      this.intent.question.splice(this.intent.question.indexOf(item), 1)
      this.intent.question = [...this.intent.question]
    },
    removeAns(item) {
      this.intent.answer.splice(this.intent.answer.indexOf(item), 1)
      this.intent.answer = [...this.intent.answer]
    },
    async todo() {
      this.spin = false
      const path = `/intents/query/update/${this.intent.id}`
      await this.$axios.put(path, this.intent)
          .then((res) => {
            this.$notifier.showMessage({
              content: `Intent updated! ${res.data.name}`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `something wrong status code ${err.response.status}`,
              color: 'red'
            })
          })
      this.spin = true
    },
    async remove() {
      this.spin = false
      this.spinSave = false
      const path = `/intents/query/delete/${this.intent.id}`
      this.$store.commit(`features/setDynamicPath`, path)
      await this.$store.dispatch(`features/deleteItem`)
      this.users.splice(this.users.indexOf(this.intent), 1)
      this.spinSave = true
      this.dialogDelete = false
      this.$notifier.showMessage({
        content: `Intent Deleted!`,
        color: 'success'
      })
      this.spin = true
    }
  },
}
</script>

<style scoped>
.v-chip {
  overflow: initial;
}
</style>