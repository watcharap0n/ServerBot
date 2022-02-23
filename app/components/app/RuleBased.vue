<template>

  <v-card class="text-center p-2" flat>

    <v-card-text>
      <v-switch
          dense
          :color="`${ruleBased.ready ? 'red': ''}`"
          v-model="ruleBased.ready"
          :label="`${ruleBased.ready ? 'Enabled': 'Disabled'}`"
      >
      </v-switch>
      <div :hidden="!ruleBased.ready">
        <p class="text-xl font-normal font-extrabold text-green-500"
           v-text="`${ruleBased.postback ? 'Postback': 'Keyword'}`"
        ></p>
        <v-switch
            dense
            :color="`${ruleBased.postback ? '#12AE7E': 'red'}`"
            v-model="ruleBased.postback"
            :label="`${ruleBased.postback ? 'Postback': 'Keyword'}`"
        >
        </v-switch>
        <v-text-field
            rounded
            v-model="ruleBased.keyword"
            :label="`${ruleBased.postback ? 'Postback': 'Keyword'}`"
            filled
            clearable
        ></v-text-field>

        <p class="text-xl font-normal font-extrabold text-green-500">Answer</p>
        <v-switch
            dense
            :color="`${ruleBased.status_flex ? '#12AE7E': 'red'}`"
            v-model="ruleBased.status_flex"
            :label="`${ruleBased.status_flex ? 'Enable Flex Message': 'Disabled Flex Message'}`"
        >
        </v-switch>

        <div v-if="!ruleBased.status_flex">
          <v-text-field
              rounded
              v-model="answer"
              label="input answer"
              filled
              @keyup.enter="sendAns"
              clearable
          ></v-text-field>
          <v-combobox
              rounded
              filled
              v-model="ruleBased.answer"
              label="answers"
              deletable-chips
              chips
              multiple
              hide-selected
              readonly
          >
            <template v-slot:selection="{ attrs, item, select, selected }">
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
            </template>
          </v-combobox>
        </div>

        <div v-else>
          <v-select
              rounded
              filled
              v-model="ruleBased.card"
              :items="cards"
              item-text="name"
              item-value="_id"
              append-outer-icon="mdi-card-bulleted-outline"
              menu-props="auto"
              hide-details
              label="select your flex messages"
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
          :loading="!spin"
          @click="todo"
      >
        <v-icon left>mdi-database-plus</v-icon>
        submit
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
    <Dialog :dialog.sync="dialog"
            header="ลบข้อมูล"
            body="are you sure delete rule based?"
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
    ruleBased: {
      required: false,
      type: Object
    },
    cards: {
      required: false
    },
    users: {
      required: false
    },
  },
  data() {
    return {
      answer: "",
      items: [],
      dialog: false,
      spin: true

    }
  },
  methods: {
    sendAns() {
      this.ruleBased.answer.push(this.answer)
      this.answer = ''
    },
    removeKeyword(item) {
      this.ruleBased.keyword.splice(this.ruleBased.keyword.indexOf(item), 1)
      this.ruleBased.keyword = [...this.ruleBased.keyword]

    },
    removeAns(item) {
      this.ruleBased.answer.splice(this.ruleBased.answer.indexOf(item), 1)
      this.ruleBased.answer = [...this.ruleBased.answer]
    },
    async remove() {
      this.spin = false
      this.spinSave = false
      const path = `/rule_based/query/delete/${this.ruleBased.id}`
      this.$store.commit(`features/setDynamicPath`, path)
      await this.$store.dispatch(`features/deleteItem`)
      this.users.splice(this.users.indexOf(this.ruleBased), 1)
      this.spinSave = true
      this.dialogDelete = false
      this.$notifier.showMessage({
        content: `deleted!`,
        color: 'success'
      })
      this.spin = true
    },
    async todo() {
      this.spin = false
      const path = `/rule_based/query/update/${this.ruleBased.id}`
      await this.$axios.put(path, this.ruleBased)
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
    }
  },

}
</script>

<style scoped>
.v-chip {
  overflow: initial;
}
</style>