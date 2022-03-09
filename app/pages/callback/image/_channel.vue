<template>
  <div class="h-auto">
    <v-card flat>
      <v-toolbar
          dense
          color="info"
          dark
          flat
      >
        <v-icon>mdi-robot-outline</v-icon>&nbsp;
        <v-toolbar-title>Map Image</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn color="white"
               @click="dialog = true"
               :hidden="!btnShow"
               text
        >
          <v-icon left>mdi-plus</v-icon>
          Add Map Image
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
                  mdi-image
                </v-icon>
                <v-icon v-else color="red">
                  mdi-image-outline
                </v-icon>
              </div>
            </template>

            <template v-slot:label="{item}">
              <div>{{ item.name }}</div>
              <small v-if="selected">{{ item.description }}</small>
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
              select item
            </div>

            <v-card
                v-else
                :key="selected.id"
                flat
            >
              <v-card-text>

                <SetImage
                    :image="selected"
                    :users.sync="users"
                />

              </v-card-text>
            </v-card>

          </v-scroll-y-transition>
        </v-col>
      </v-row>
    </v-card>
    <Dialog :dialog.sync="dialog"
            header="Mapping"
            :element-forms="elements"
            max-width="450"
            body="Please set your name Mapping!"
            :loading-dialog="!spinSave"
            :submit-dialog="save"
    />


  </div>
</template>

<script>
import Dialog from "@/components/app/Dialog";
import SetImage from "@/components/app/Image";

export default {
  components: {Dialog, SetImage},
  data() {
    return {
      mapping: [],
      dialog: false,
      dialogDelete: false,
      spinSave: true,
      btnShow: false,
      setName: '',
      form: {
        name: '',
        access_token: '',
        content: '',
        description: '',
        base_url_image: ''
      },
      defaultForm: {
        name: '',
        access_token: '',
        content: '',
        description: '',
        base_url_image: ''
      },
      data: [],
      active: [],
      avatar: null,
      open: [],
      users: [],
      elements: [
        {
          color: 'primary',
          label: 'Name Mapping',
          rules: [v => !!v || 'required!'],
          icon: 'mdi-robot',
          value: this.setName
        }
      ]
    }
  },
  computed: {
    items() {
      return [
        {
          name: 'My Map Images',
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
      const path = `/mapping/?access_token=${encoded}`;
      await this.$axios.get(path)
          .then((res) => {
            res.data.forEach((v) => {
              v.id = v._id
            })
            item.children.push(...res.data);
            this.getMapping(encoded);
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
              content: `something wrong! ${err.response.status}`,
              color: 'red'
            })
            console.error(err);
          })
    },
    async save() {
      this.spinSave = true
      await this.fetchToken()
      this.form.name = this.elements[0].value
      const path = '/mapping/create'
      this.$axios.post(path, this.form)
          .then((res) => {
            this.form = res.data
            this.form.id = this.form._id
            this.users.push(this.form)
            this.form = Object.assign({}, this.defaultForm)
            this.$notifier.showMessage({
              content: 'create mapping successfully',
              color: 'success'
            })
            console.log(res.data)
          })
          .catch((err) => {
            console.error(err)
            if (err.response.status === 400) {
              this.$notifier.showMessage({
                content: `data mapping duplicate!  ${this.form.name}`,
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
    async getMapping(accessToken) {
      const path = `/mapping/?access_token=${accessToken}`
      this.$store.commit('features/setDynamicPath', path)
      await this.$store.dispatch('features/fetchCard')
      this.mapping = this.$store.getters["features/getResponse"]
    },

  },

}
</script>

<style scoped>
</style>