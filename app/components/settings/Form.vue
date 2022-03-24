<template>
  <div>

    <v-row>
      <v-col
          v-for="(v, k) in transactions"
          :key="k"
          sm="6"
      >
        <v-text-field
            dense
            v-model="v.name"
            outlined
            rounded
            label="Name"
        >
        </v-text-field>

        <v-spacer></v-spacer>

        <v-btn
            class="text-decoration-none"
            dark
            small
            :to="`/callback/custom/form/${$route.params.channel}?q=${v._id}`"
            color="info"
            rounded
        >
          <v-icon left>
            mdi-rocket-launch
          </v-icon>
          form
        </v-btn>

        <v-btn
            color="success"
            rounded
            @click="todo(v)"
            :loading="spinSave"
            small
        >
          <v-icon left>
            mdi-pencil
          </v-icon>
          save
        </v-btn>

        <v-btn
            dark
            small
            @click="remove(v)"
            color="grey"
            rounded
            :loading="spinDelete"
        >
          <v-icon left>
            mdi-eraser
          </v-icon>
          remove
        </v-btn>
      </v-col>

      <v-col>
        <v-btn
            @click="dialog = true"
            class="mx-2"
            fab
            dark
            small
            color="success"
        >
          <v-icon dark>
            mdi-plus
          </v-icon>
        </v-btn>
      </v-col>

    </v-row>

    <Dialog :dialog.sync="dialog"
            header="Form"
            :element-forms="elements"
            max-width="450"
            body="Please set your id form"
            :submit-dialog="addTransaction"
            :loading-dialog="spinDialog"
    />

    <Overlay :overlay="overlay"></Overlay>

  </div>
</template>

<script>
import Dialog from "@/components/app/Dialog";
import Overlay from "@/components/app/Overlay"

export default {
  components: {
    Dialog,
    Overlay,
  },

  data() {
    return {
      dialog: false,
      valid: false,
      transactions: [],
      defaultForm: {
        name: '',
        endpoint: '',
        access_token: '',
      },
      overlay: false,
      spinSave: false,
      spinDelete: false,
      spinDialog: false,
      elements: [
        {
          color: 'info',
          label: 'Name',
          value: ''
        }
      ],
      encoded: '',
    }
  },

  async created() {
    this.overlay = true;
    const pathToken = `/callback/channel/info/${this.$route.params.channel}`;
    this.$store.commit('features/setDynamicPath', pathToken);
    await this.$store.dispatch('features/fetchToken');
    this.defaultForm.access_token = this.$store.getters["features/getToken"];

    let encoded = encodeURIComponent(this.defaultForm.access_token);
    this.encoded = encoded;
    const path = `/form/find?access_token=${encoded}`;
    await this.$axios.get(path)
        .then((res) => {
          this.transactions = res.data;
        })
        .catch((err) => {
          console.error(err);
        })
    this.overlay = false;
  },

  methods: {
    async addTransaction() {
      this.spinDialog = true
      this.defaultForm.name = this.elements[0].value
      await this.$axios.post('/form/create', this.defaultForm)
          .then((res) => {
            this.transactions.push(res.data);
            this.$notifier.showMessage({
              content: `add form is successfully`,
              color: 'success'
            })
          })
          .catch((err) => {
            console.error(err)
            if (err.response.status === 400) {
              this.$notifier.showMessage({
                content: `duplicate form id!`,
                color: 'red'
              })
            } else {
              this.$notifier.showMessage({
                content: `something wrong! ${err.response.status}`,
                color: 'red'
              })
            }
          })
      this.spinDialog = false
      this.dialog = false;
      this.elements[0].value = ''
    },

    async remove(item) {
      this.spinDelete = true;
      const path = `/form/query/delete/${item._id}`
      await this.$axios.delete(path)
          .then((res) => {
            this.transactions.splice(this.transactions.indexOf(item), 1);
            this.$notifier.showMessage({
              content: `deleted ${item.value} | status code ${res.status}!`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `something wrong | ${err.response.status}`,
              color: 'red'
            })
          })
      this.spinDelete = false;
    },

    async todo(item) {
      this.spinSave = true;
      const path = `/form/query/update/${item._id}`
      await this.$axios.put(path, item)
          .then((res) => {
            this.$notifier.showMessage({
              content: `updated form`,
              color: 'success'
            })
            console.log(res.data);
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `${err.response.data.detail} | status code ${err.response.status}`,
              color: 'red'
            })
            console.error(err);
          })
      this.spinSave = false;

    }
  }
}
</script>

<style scoped>
</style>

