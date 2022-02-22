<template>
  <div class="h-auto">
    <v-card>
      <v-toolbar
          color="#12AE7E"
          dark
          flat
      >
        <v-icon>mdi-card-plus</v-icon>&nbsp;
        <v-toolbar-title>การ์ด</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn color="info"
               rounded
               @click="dialog = true"
               :hidden="!btnShow"
        >
          <v-icon left>mdi-card-plus-outline</v-icon>
          เพิ่มการ์ด
        </v-btn>

      </v-toolbar>
      <v-row
          class="pa-4"
          justify="space-between"
      >
        <v-col cols="12" sm="4">
          <v-treeview
              :active.sync="active"
              :items="items"
              :load-children="fetchItems"
              :open.sync="open"
              activatable
              color="info"
              open-on-click
              transition
          >
            <template v-slot:prepend="{ item }">
              <v-icon v-if="!item.children" color="info">
                mdi-card
              </v-icon>
            </template>

            <template v-slot:label="{item}">
              <div>{{ item.name }}</div>
              <small v-if="selected">{{ item.message }}</small>
            </template>

          </v-treeview>
        </v-col>

        <v-col
            cols="12" sm="8"
        >
          <v-scroll-y-transition mode="out-in">
            <div
                v-if="!selected"
                class="text-h6 grey--text text--lighten-1 font-weight-light"
                style="align-self: center;"
            >
              เลือกรายการ
            </div>
            <v-card
                v-else
                :key="selected.id"
                flat
            >
              <v-card-text>
                <Card
                    :spin="!spinSave"
                    v-if="selected"
                    :delete-card="deleteCard"
                    :update-card="todo"
                    :set-object="selected" @input="selected = $event"
                />
              </v-card-text>

            </v-card>
          </v-scroll-y-transition>
        </v-col>
      </v-row>
    </v-card>
    <Dialog :dialog.sync="dialog"
            header="เพิ่มการ์ด"
            :element-forms="elements"
            max-width="450"
            body="กรุณาตั้งชื่อการ์ดเพิ่มสร้างการ์ดของท่าน"
            :loading-dialog="spinSave"
            :submit-dialog="save"
    />


    <Dialog :dialog.sync="dialogDelete"
            header="ลบข้อมูล"
            body="คุณแน่ใจว่าจะลบข้อมูล ?"
            max-width="350"
            :loading-dialog="spinSave"
            :submit-dialog="remove"
    />
  </div>
</template>

<script>

import Dialog from "@/components/app/Dialog";
import Card from "@/components/app/Card";

export default {
  components: {Dialog, Card},
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      spinSave: false,
      btnShow: false,
      setName: '',
      form: {
        name: '',
        access_token: '',
        content: '',
        message: '',
      },
      defaultForm: {
        name: '',
        access_token: '',
        content: '',
        message: '',
      },
      data: [],
      active: [],
      avatar: null,
      open: [],
      users: [],
      elements: [
        {
          color: 'primary',
          label: 'ตั้งชื่อการ์ด',
          rules: [v => !!v || 'กรุณากรอกข้อมูล'],
          icon: 'mdi-card-plus',
          value: this.setName
        }
      ]
    }
  },
  async created() {
    await this.$parent.$emit('routerHandle', this.$route.params);
  },
  computed: {
    items() {
      return [
        {
          name: 'การ์ดของฉัน',
          children: this.users,
        },
      ]
    },
    selected() {
      if (!this.active.length) return undefined
      const id = this.active[0]
      return this.users.find(user => user.id === id)
    },
  },
  methods: {
    async fetchItems(item) {
      if (this.item) return

      await this.fetchToken()
      let encoded = encodeURIComponent(this.form.access_token);
      const path = `/card/?access_token=${encoded}`;
      await this.$axios.get(path)
          .then((res) => {
            res.data.forEach((v) => {
              v.id = v._id
            })
            item.children.push(...res.data);
          })
          .catch((err) => {
            console.error(err);
          })
      this.btnShow = true;
    },
    async fetchToken() {
      const path = `/callback/channel/info/${this.$route.params.channel}`;
      await this.$axios.get(path)
          .then((res) => {
            this.form.access_token = res.data.access_token
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: 'มีบางอย่างผิดพลาด',
              color: 'red'
            })
            console.error(err);
          })
    },
    async save() {
      this.spinSave = true
      await this.fetchToken()
      this.form.name = this.elements[0].value
      const path = '/card/create'
      await this.$axios.post(path, this.form)
          .then((res) => {
            this.form = res.data
            this.form.id = this.form._id
            this.users.push(this.form)
            this.form = Object.assign({}, this.defaultForm)
            this.$notifier.showMessage({
              content: 'สร้างการ์ดสำเร็จ คุณสามารถกำหนดรูปแบบได้แล้ว',
              color: 'success'
            })
          })
          .catch((err) => {
            console.error(err)
            if (err.response.status === 400) {
              this.$notifier.showMessage({
                content: `ชื่อการ์ดนี้เคยมีการสร้างแล้ว  ${this.form.name}`,
                color: 'red'
              })
            } else {
              this.$notifier.showMessage({
                content: `มีบางอย่างผิดพลาด! ${err.response.status}`,
                color: 'red'
              })
            }
          })
      this.dialog = false;
      this.spinSave = false
      this.elements[0].value = ''
    },
    deleteCard() {
      this.dialogDelete = true
    },
    async remove() {
      this.spinSave = true
      const path = `/card/query/delete/${this.selected._id}`
      this.$store.commit('features/setDynamicPath', path)
      await this.$store.dispatch('features/deleteItem')
      this.users.splice(this.users.indexOf(this.selected), 1)
      this.spinSave = false
      this.dialogDelete = false
      this.$notifier.showMessage({
        content: `ลบการ์ดแล้ว!`,
        color: 'success'
      })
    },
    async todo() {
      this.spinSave = true
      this.form = Object.assign({}, this.selected)
      const path = `/card/query/update/${this.selected._id}`;
      await this.$axios.put(path, this.form)
          .then(() => {
            this.$notifier.showMessage({
              content: `แก้ไขการ์ดแล้ว!`,
              color: 'success'
            })
            this.form = Object.assign({}, this.defaultForm)
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `มีบางอย่างผิดพลาด status code ${err.response.status}`,
              color: 'red'
            })
          })
      this.spinSave = false
    }
  }
}
</script>

<style scoped>
</style>