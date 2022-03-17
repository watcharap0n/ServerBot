<template>
  <div>

    <v-card flat>
      <v-toolbar
          dense
          color="info"
          dark
          flat
      >
        <v-icon>mdi-dice-5-outline</v-icon>&nbsp;
        <v-toolbar-title>Rule Based</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn color="white"
               @click="dialog = true"
               :hidden="!btnShow"
               text
        >
          <v-icon left>mdi-plus</v-icon>
          Add Rule Based
        </v-btn>

      </v-toolbar>
      <v-row
          class="pa-4"
          justify="space-between"
      >
        <v-col cols="12" sm="4">
          <v-treeview
              dense
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
              <div v-if="!item.children && selected">
                <v-icon v-if="item.id === selected.id" color="red">
                  mdi-dice-5
                </v-icon>
                <v-icon v-else color="red">
                  mdi-dice-5-outline
                </v-icon>
              </div>
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
              selecte item
            </div>
            <v-card
                v-else
                :key="selected.id"
                flat
            >
              <v-card-text>

                <RuleBased
                    :rule-based="selected"
                    :cards="cards"
                    :users.sync="users"
                    :images="images"
                    :spin-get-type.sync="spinGetType"
                    :get-type.sync="getType"
                />

              </v-card-text>

            </v-card>
          </v-scroll-y-transition>
        </v-col>
      </v-row>
    </v-card>

    <Dialog :dialog.sync="dialog"
            header="Add Rule Based"
            :element-forms="elements"
            max-width="450"
            body="Please set your name Rule Based!"
            :loading-dialog="!spinSave"
            :submit-dialog="save"
    />

  </div>
</template>

<script>
import Dialog from "@/components/app/Dialog";
import RuleBased from "@/components/callback/RuleBased";

export default {
  components: {Dialog, RuleBased},
  data() {
    return {
      spinGetType: false,
      cards: [],
      images: [],
      dialog: false,
      dialogDelete: false,
      spinSave: true,
      btnShow: false,
      setName: '',
      encoded: '',
      form: {
        name: '',
        access_token: '',
        status_flex: false,
        ready: true,
        card: "",
        keyword: "",
        answer: []
      },
      defaultForm: {
        name: '',
        access_token: '',
        status_flex: false,
        ready: true,
        card: "",
        keyword: "",
        answer: []
      },
      data: [],
      active: [],
      avatar: null,
      open: [],
      users: [],
      elements: [
        {
          color: 'primary',
          label: 'Name Rule Based',
          rules: [v => !!v || 'กรุณากรอกข้อมูล'],
          icon: 'mdi-dice-5-outline',
          value: this.setName
        }
      ]
    }
  },

  computed: {
    items() {
      return [
        {
          name: 'My Rule Based',
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

  async created() {
    await this.$parent.$emit('routerHandle', this.$route.params);
  },

  methods: {
    async fetchItems(item) {
      if (this.item) return

      await this.fetchToken()
      let encoded = encodeURIComponent(this.form.access_token);
      const path = `/rule_based/?access_token=${encoded}`;
      this.encoded = encoded
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
              content: `something wrong ${err.response.status} `,
              color: 'red'
            })
            console.error(err);
          })
    },

    async save() {
      this.spinSave = false
      await this.fetchToken()
      this.form.name = this.elements[0].value
      const path = '/rule_based/create'
      this.$axios.post(path, this.form)
          .then((res) => {
            this.form = res.data
            this.form.id = this.form._id
            this.users.push(this.form)
            this.form = Object.assign({}, this.defaultForm)
            this.$notifier.showMessage({
              content: 'created rule-based successfully',
              color: 'success'
            })
          })
          .catch((err) => {
            console.error(err)
            if (err.response.status === 400) {
              this.$notifier.showMessage({
                content: `duplicate name rule-based  ${this.form.name}`,
                color: 'red'
              })
            } else {
              this.$notifier.showMessage({
                content: `something wrong! ${err.response.status}`,
                color: 'red'
              })
            }
          })
      this.dialog = false;
      this.spinSave = true
      this.elements[0].value = ''
    },

    async getCards() {
      const path = `/card?access_token=${this.encoded}`
      this.$store.commit('features/setDynamicPath', path)
      await this.$store.dispatch('features/fetchCard')
      this.cards = this.$store.getters["features/getResponse"]
    },

    async getImageMap() {
      const path = `/mapping?access_token=${this.encoded}`
      this.$store.commit('features/setDynamicPath', path)
      await this.$store.dispatch('features/fetchCard')
      this.images = this.$store.getters["features/getResponse"]
    },

    async getType(type) {
      if (type === 'Flex Message') {
        this.spinGetType = true;
        await this.getCards();
        this.spinGetType = false;
      } else if (type === 'Image Map') {
        this.spinGetType = true
        await this.getImageMap();
        this.spinGetType = false;
      }
    }

  },


}
</script>

<style scoped>
</style>