<template>

  <v-card class="text-center p-2" flat>

    <v-card-text>
      <div :hidden="!ruleBased.ready">
        <p class="text-l font-normal  "
           v-text="`${ruleBased.postback ? 'Postback': 'Keyword'}`"
        ></p>

        <v-switch
            dense
            color="info"
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

        <p class="text-l font-normal  ">Answer</p>

        <v-select
            filled
            rounded
            v-model="ruleBased.type_reply"
            label="Type Reply"
            color="info"
            :items="typeReply"
            @change="getType(ruleBased.type_reply)"
        >
        </v-select>

        <div v-if="ruleBased.type_reply === 'Text'">
          <v-text-field
              rounded
              v-model="answer"
              label="input answer"
              filled
              @keyup.enter="sendAns"
              clearable
          ></v-text-field>

          <v-combobox
              v-model="ruleBased.answer"
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
                (+{{ ruleBased.answer.length - 2 }} others)
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
                    @click:close="removeAns(item)"
                >
                  <strong>{{ item }}</strong>&nbsp;
                </v-chip>
              </div>
            </template>
          </v-combobox>
        </div>

        <div v-else-if="ruleBased.type_reply === 'Flex Message'">
          <v-select
              rounded
              :loading="spinGetType"
              filled
              v-model="ruleBased.card"
              :items="cards"
              item-text="name"
              color="info"
              item-value="_id"
              append-outer-icon="mdi-card-bulleted-outline"
              menu-props="auto"
              item-color="info"
              hide-details
              label="select your flex message"
              single-line
          ></v-select>
        </div>

        <div v-else-if="ruleBased.type_reply === 'Image Map'">
          <v-select
              rounded
              :loading="spinGetType"
              filled
              v-model="ruleBased.image"
              :items="images"
              item-text="name"
              color="info"
              item-value="_id"
              append-outer-icon="mdi-card-bulleted-outline"
              menu-props="auto"
              item-color="info"
              hide-details
              label="select your image map"
              single-line
          ></v-select>
        </div>
      </div>
    </v-card-text>

    <v-card-actions>

      <v-switch
          dense
          color="info"
          v-model="ruleBased.ready"
          :label="`${ruleBased.ready ? 'Enabled': 'Disabled'}`"
      >
      </v-switch>

      <v-spacer></v-spacer>

      <v-btn
          text
          color="info"
          :loading="!spin"
          @click="todo"
      >
        <v-icon left>mdi-database-plus</v-icon>
        save
      </v-btn>
      <v-btn
          text
          color="grey"
          dark
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
    images: {
      required: true,
    },
    spinGetType: {
      required: false,
      type: Boolean
    },
    getType: {
      required: true,
    },
  },

  data() {
    return {
      typeReply: ['Text', 'Flex Message', 'Image Map'],
      show: false,
      answer: "",
      items: [],
      dialog: false,
      spin: true

    }
  },

  created() {
    if (this.ruleBased) {
      this.$nextTick(() => {
        this.getType(this.ruleBased.type_reply)
      })
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