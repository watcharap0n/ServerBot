<template>
  <div>

    <v-row>
      <v-col
          v-for="(v, k) in transactions"
          :key="k"
          sm="6"
      >
        <v-text-field
            v-model="v.name"
            outlined
            rounded
            label="Name"
        >
        </v-text-field>
        <v-spacer></v-spacer>
        <v-btn
            v-model="v.endpoint"
            color="orange"
            rounded
        >
          <v-icon left>
            mdi-rocket-launch
          </v-icon>
          go to form

        </v-btn>

        <v-btn
            @click="remove(v)"
            color="red"
            rounded
        >
          <v-icon left>
            mdi-eraser
          </v-icon>
          remove
        </v-btn>

        <v-btn
            color="success"
            rounded
            @click="todo(v)"
            :loading="spin"
        >
          <v-icon left>
            mdi-pencil
          </v-icon>
          save

        </v-btn>


      </v-col>
      <v-col>
        <v-btn
            @click="dialog = true"
            class="mx-2"
            fab
            dark
            color="indigo"
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

    />
  </div>
</template>

<script>
import Dialog from "@/components/app/Dialog";

export default {
  components: {Dialog},
  data() {
    return {
      dialog: false,
      valid: false,
      transactions: [],
      form: {
        name: '',
        id_form: '',
        models: [],
        endpoint: '',
        access_token: '',
      },
      defaultForm: {
        name: '',
        id_form: '',
        models: [],
        endpoint: '',
        access_token: '',
      },
      spin: false,
      loading: false,
      elements: [
        {
          color: 'primary',
          label: 'id form',
          value: this.setId
        }
      ],
      setId: '',



    }
  },
  async created() {
    this.loading = true;
    const pathToken = `/callback/channel/info/${this.$route.params.channel}`;
    this.$store.commit('features/setDynamicPath', pathToken);
    await this.$store.dispatch('features/fetchToken');
    this.defaultForm.access_token = this.$store.getters["features/getToken"];

    let encoded = encodeURIComponent(this.defaultForm.access_token);
    const path = `/form/?access_token=${encoded}`;
    await this.$axios.get(path)
        .then((res) => {
          this.transactions = res.data;
        })
        .catch((err) => {
          console.error(err);
        })
    this.loading = false;
  },
  methods: {
    async addTransaction() {
      this.loading = true;
      this.defaultForm.id_form = this.elements[0].value
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
                content: `id form duplicate!`,
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
      this.loading = false
      this.elements[0].value = ''
    },
    async remove(item) {
      this.loading = true
      const path = `/form/query/delete/${item._id}`
      await this.$axios.delete(path)
          .then((res) => {
            this.transactions.splice(this.transactions.indexOf(item), 1)
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
      this.loading = false;
    },
    async todo(item) {
      this.spin = true
      const path = `/form/query/update/${item._id}`
      await this.$axios.put(path, item)
          .then((res) => {
            this.$notifier.showMessage({
              content: `updated form`,
              color: 'success'
            })
            console.log(res.data)
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `${err.response.data.detail} | status code ${err.response.status}`,
              color: 'red'
            })
            console.error(err);
          })
      this.spin = false

    }

  }
}
</script>

<style scoped>
</style>

