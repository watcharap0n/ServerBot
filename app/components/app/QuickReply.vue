<template>

  <v-card class="text-center p-2" flat>
    <v-card-text>
      <p class="text-xl font-normal font-extrabold">Quick Reply</p>
      <v-select
          rounded
          filled
          v-model="button.intent"
          :items="intent"
          item-text="name"
          item-value="_id"
          label="Select you intents"
      ></v-select>
      <v-text-field
          rounded
          filled
          v-model="reply"
          @keydown.enter="sendReply"
          label="input answer"
      >
      </v-text-field>
      <v-combobox
          v-model="button.reply"
          label="Answers"
          :items="button.reply"
          chips
          multiple
          hide-selected
          readonly
      >
        <template v-slot:append-outer>
          <v-btn icon
                 color="info"
                 @click="show1 = !show1"
          >
            <v-icon
                v-text="`${show1 ? 'mdi-format-vertical-align-center' : 'mdi-format-line-spacing'}`"
            ></v-icon>
          </v-btn>
        </template>
        <template v-slot:selection="{ attrs, item, select, selected, index }">
          <div v-if="!show1">
            <v-chip
                v-if="index <= 3"
                dark
                color="info"
                v-bind="attrs"
                :input-value="selected"
                close
                @click="select"
                @click:close="removeReply(item)"
            >
              <strong>{{ item }}</strong>&nbsp;
            </v-chip>
            <span v-if="index === 4"
                  class="grey--text text-caption"
            >
                (+{{ button.reply.length - 4 }} others)
              </span>
          </div>
          <div v-else-if="show1">
            <v-chip
                dark
                color="info"
                v-bind="attrs"
                :input-value="selected"
                close
                @click="select"
                @click:close="removeReply(item)"
            >
              <strong>{{ item }}</strong>&nbsp;
            </v-chip>
          </div>
        </template>
      </v-combobox>

      <p class="text-xl font-normal font-extrabold ">Label</p>
      <v-text-field
          rounded
          filled
          v-model="label"
          @keydown.enter="sendLabel"
          label="input label"
      >
      </v-text-field>
      <v-combobox
          v-model="button.labels"
          label="Labels"
          :items="button.labels"
          chips
          multiple
          hide-selected
          readonly
      >
        <template v-slot:append-outer>
          <v-btn icon
                 color="info"
                 @click="show2 = !show2"
          >
            <v-icon
                v-text="`${show2 ? 'mdi-format-vertical-align-center' : 'mdi-format-line-spacing'}`"
            ></v-icon>
          </v-btn>
        </template>

        <template v-slot:selection="{ attrs, item, select, selected, index }">
          <div v-if="!show2">
            <v-chip
                v-if="index <= 3"
                dark
                color="info"
                v-bind="attrs"
                :input-value="selected"
                close
                @click="select"
                @click:close="removeLabel(item)"
            >
              <strong>{{ item }}</strong>&nbsp;
            </v-chip>
            <span v-if="index === 4"
                  class="grey--text text-caption"
            >
                (+{{ button.labels.length - 4 }} others)
              </span>
          </div>
          <div v-else-if="show2">
            <v-chip
                dark
                color="info"
                v-bind="attrs"
                :input-value="selected"
                close
                @click="select"
                @click:close="removeLabel(item)"
            >
              <strong>{{ item }}</strong>&nbsp;
            </v-chip>
          </div>
        </template>
      </v-combobox>

      <p class="text-xl font-normal font-extrabold ">label</p>
      <v-text-field
          rounded
          filled
          v-model="text"
          @keydown.enter="sendTexts"
          label="input text"
      >
      </v-text-field>
      <v-combobox
          v-model="button.texts"
          label="Texts"
          :items="button.texts"
          chips
          multiple
          hide-selected
          readonly
      >
        <template v-slot:append-outer>
          <v-btn icon
                 color="info"
                 @click="show3 = !show3"
          >
            <v-icon
                v-text="`${show3 ? 'mdi-format-vertical-align-center' : 'mdi-format-line-spacing'}`"
            ></v-icon>
          </v-btn>
        </template>

        <template v-slot:selection="{ attrs, item, select, selected, index }">
          <div v-if="!show3">
            <v-chip
                v-if="index <= 3"
                dark
                color="info"
                v-bind="attrs"
                :input-value="selected"
                close
                @click="select"
                @click:close="removeTexts(item)"
            >
              <strong>{{ item }}</strong>&nbsp;
            </v-chip>
            <span v-if="index === 4"
                  class="grey--text text-caption"
            >
                (+{{ button.texts.length - 4 }} others)
              </span>
          </div>
          <div v-else-if="show3">
            <v-chip
                dark
                color="info"
                v-bind="attrs"
                :input-value="selected"
                close
                @click="select"
                @click:close="removeTexts(item)"
            >
              <strong>{{ item }}</strong>&nbsp;
            </v-chip>
          </div>
        </template>
      </v-combobox>

    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
          color="success"
          text
          x-large
          :loading="!spin"
          @click="todo"
      >submit
      </v-btn>
      <v-btn
          color="red"
          dark
          text
          @click="dialog = true"
      >
        <v-icon left>mdi-delete</v-icon>
        delete
      </v-btn>
    </v-card-actions>

    <Dialog
        :dialog.sync="dialog"
        header="delete!"
        body="are you sure delete ?"
        max-width="350"
        :loading-dialog="!spin"
        :submit-dialog="remove"
    />
  </v-card>


</template>

<script>

import Dialog from "@/components/app/Dialog";


export default {
  components: {Dialog},
  props: {
    button: {
      required: false,
      type: Object
    },
    users: {
      required: false
    },
    intent: {
      required: false
    }
  },
  data() {
    return {
      show1: false,
      show2: false,
      show3: false,
      dialog: false,
      spin: true,
      selected: "",
      text: "",
      label: "",
      reply: ""
    }
  },
  methods: {
    sendTexts() {
      this.button.texts.push(this.text)
      this.text = ''
    },
    sendLabel() {
      this.button.labels.push(this.label)
      this.label = ''
    },
    sendReply() {
      this.button.reply.push(this.reply)
      this.reply = ''
    },
    removeTexts(item) {
      this.button.texts.splice(this.button.texts.indexOf(item), 1)
      this.button.texts = [...this.button.texts]
    },
    removeLabel(item) {
      this.button.labels.splice(this.button.labels.indexOf(item), 1)
      this.button.labels = [...this.button.labels]
    },
    removeReply(item) {
      this.button.reply.splice(this.button.reply.indexOf(item), 1)
      this.button.reply = [...this.button.reply]
    },
    async remove() {
      this.spin = false
      this.spinSave = false
      const path = `/button/query/delete/${this.button.id}`
      this.$store.commit(`features/setDynamicPath`, path)
      await this.$store.dispatch(`features/deleteItem`)
      this.users.splice(this.users.indexOf(this.button), 1)
      this.spinSave = true
      this.dialogDelete = false
      this.$notifier.showMessage({
        content: `deleted!`,
        color: 'red'
      })
      this.spin = true
    },
    async todo() {
      if (this.button.texts.length === this.button.labels.length) {
        this.spin = false
        const path = `/button/query/update/${this.button.id}`
        await this.$axios.put(path, this.button)
            .then((res) => {
              this.$notifier.showMessage({
                content: `updated ${res.data.name}`,
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
      } else {
        this.$notifier.showMessage({
          content: `Please enter text and labels. equal!`,
          color: 'red'
        })

      }
    }
  }
}
</script>

<style scoped>
</style>