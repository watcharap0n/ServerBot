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
              :items="cards"
              item-text="name"
              item-value="_id"
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
          :loading="!spin"
          @click="todo"
      >
        <v-icon left>mdi-database-plus</v-icon>
        บันทึกข้อมูล
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
    <Dialog :dialog.sync="dialog"
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
  components:{Dialog},
  props: {
    ruleBased:{
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
        content: `ลบกฎแล้ว!`,
        color: 'success'
      })
      this.spin = true
    },
    async todo(){
      this.spin = false
      const path = `/rule_based/query/update/${this.ruleBased.id}`
      await this.$axios.put(path, this.ruleBased)
       .then((res) => {
         this.$notifier.showMessage({
              content: `แก้ไขกฎแล้ว ${res.data.name}`,
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
    }
  },

}
</script>

<style scoped>
.v-chip {
  overflow: initial;
}
</style>