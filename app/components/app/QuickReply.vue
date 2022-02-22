<template>
  <v-card class="text-center p-2" flat>
    <v-card-text>
      <p class="text-xl font-normal font-extrabold text-green-500">ตอบเร็ว</p>
      <v-select
          v-model="button.intent"
          :items="intent"
          item-text="name"
          item-value="_id"
          label="เลือกสอนบอทที่ต้องการสร้างตอบเร็ว"
      ></v-select>
      <v-text-field
          v-model="reply"
          @keydown.enter="sendReply"
          label="ตอบเร็ว"
      >
      </v-text-field>
      <v-combobox
          v-model="button.reply"
          label="แสดงตอบเร็ว"
          :items="button.reply"
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
              @click:close="removeReply(item)"
          >
            <strong>{{ item }}</strong>&nbsp;

          </v-chip>
        </template>
      </v-combobox>

      <p class="text-xl font-normal font-extrabold text-green-500">ข้อความ</p>
      <v-text-field
          v-model="label"
          @keydown.enter="sendLabel"
          label="ข้อความ"
      >
      </v-text-field>
      <v-combobox
          v-model="button.labels"
          label="แสดงข้อความ"
          :items="button.labels"
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
              @click:close="removeLabel(item)"
          >
            <strong>{{ item }}</strong>&nbsp;

          </v-chip>
        </template>
      </v-combobox>

      <p class="text-xl font-normal font-extrabold text-green-500">ป้าย</p>
      <v-text-field
          v-model="text"
          @keydown.enter="sendTexts"
          label="ข้อความที่ส่งไป"
      >
      </v-text-field>
      <v-combobox
          v-model="button.texts"
          label="แสดงข้อความที่ส่งไป"
          :items="button.texts"
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
              @click:close="removeTexts(item)"
          >
            <strong>{{ item }}</strong>&nbsp;

          </v-chip>
        </template>
      </v-combobox>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
          color="#12AE7E"
          text
          x-large
          :loading="!spin"
          @click="todo"
      >บันทึกข้อมูล
      </v-btn>
      <v-btn
          color="red"
          dark
          text
          @click="dialog = true"
      >
        <v-icon left>mdi-delete</v-icon>
        ลบข้อมูล
      </v-btn>
    </v-card-actions>
    <Dialog
        :dialog.sync="dialog"
        header="ลบข้อมูล"
        body="คุณแน่ใจว่าจะลบข้อมูล ?"
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
        content: `ลบตอบเร็วแล้ว!`,
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
                content: `แก้ไขตอบเร็วแล้ว ${res.data.name}`,
                color: 'success'
              })
            })
            .catch((err) => {
              this.$notifier.showMessage({
                content: `มีบางอย่างผิดพลาด status code ${err.response.status}`,
                color: 'red'
              })
            })
        this.spin = true
      } else {
        this.$notifier.showMessage({
          content: `กรุณาใส่จำนวน ข้อความและจำนวนป้าย ให้มีจำนวนเท่ากันด้วย`,
          color: 'red'
        })

      }
    }
  }
}
</script>

<style scoped>
</style>