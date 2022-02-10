<template>
  <v-container>
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
          <v-icon left>mdi-plus</v-icon>
          เพิ่มการ์ด
        </v-btn>

      </v-toolbar>
      <v-row
          class="pa-4"
          justify="space-between"
      >
        <v-col cols="5">
          <v-treeview
              :active.sync="active"
              :items="items"
              :load-children="fetchItems"
              :open.sync="open"
              activatable
              color="warning"
              open-on-click
              transition
          >
            <template v-slot:prepend="{ item }">
              <v-icon v-if="!item.children" color="info">
                mdi-card
              </v-icon>
            </template>

          </v-treeview>
        </v-col>

        <v-col
            class="d-flex text-center"
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
                class="pt-6 mx-auto"
                flat
                max-width="400"
            >
              <v-card-text>

                {{ selected }}

              </v-card-text>
              <v-divider></v-divider>

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
            :loading-dialog="!spinSave"
            :submit-dialog="save"
    />
    <Dialog :dialog.sync="dialogDelete"
            header="ลบข้อมูล"
            body="คุณแน่ใจว่าจะลบข้อมูล ?"
            max-width="350"
            :loading-dialog="!spinSave"
            :submit-dialog="deleted"
    />
  </v-container>
</template>

<script>
import {mapGetters} from "vuex";
import Dialog from "@/components/app/Dialog";

export default {
  components: {Dialog},
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      spinSave: true,
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
    ...mapGetters({
      cards: "treeview/getInitialized",
    })
  },
  methods: {
    async fetchItems(item) {
      if (this.item) return

      await this.fetchToken()
      let encoded = encodeURIComponent(this.form.access_token);
      const path = `/card/?access_token=${encoded}`;
      this.$store.commit('treeview/setPath', path);
      await this.$store.dispatch('treeview/initialized');
      await item.children.push(...this.cards);
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
      await this.fetchToken()
      this.spinSave = false
      this.form.name = this.elements[0].value
      this.$store.commit('card/payload', this.form)
      await this.$store.dispatch('card/crateCard')
      this.form = this.$store.getters["card/getResponse"]
      this.users.push(this.form)
      this.$notifier.showMessage({
        content: 'สร้างการ์ดสำเร็จ คุณสามารถกำหนดรูปแบบได้แล้ว',
        color: 'success'
      })
      this.form = Object.assign({}, this.defaultForm)
      this.dialog = false;
      this.spinSave = true
      this.elements[0].value = ''
    },
    deleteCard(item) {
      this.dialogDelete = true
      this.$store.commit('card/setDynamicPath', item.id)
    },
    async deleted() {
      this.spinSave = false
      await this.$store.dispatch('card/deleteCard')
      this.users.splice(this.users.indexOf(this.selected), 1)
      this.spinSave = true
      this.dialogDelete = false
      this.$notifier.showMessage({
        content: `ลบการ์ดแล้ว`,
        color: 'success'
      })
    }
  },
}
</script>

<style scoped>
</style>