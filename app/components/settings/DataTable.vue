<template>

  <div>

    <v-row>
      <v-col
          v-if="transactions.length > 0"
          v-for="(v, k) in transactions"
          :key="k"
          sm="10">

        <v-card
        >
          <v-form>

            <v-card-text>
              <v-row>

                <v-col cols="12"
                       sm="6"
                >
                  <v-text-field
                      dense
                      outlined
                      rounded
                      hint="Set your name column, example Name"
                      persistent-hint
                      label="Text"
                      v-model="v.text"
                      color="info"
                  ></v-text-field>
                </v-col>

                <v-col cols="12"
                       sm="6"
                >
                  <v-text-field
                      dense
                      outlined
                      rounded
                      hint="Set your value for save data, example name"
                      persistent-hint
                      label="Value"
                      v-model="v.value"
                      color="info"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  @click="remove(v)"
                  small
                  color="grey">
                Remove
              </v-btn>
              <v-btn
                  @click="save(v)"
                  small
                  :loading="spin"
                  color="info">
                Save
              </v-btn>
            </v-card-actions>

          </v-form>
        </v-card>

      </v-col>

      <v-col sm="2">
        <v-btn
            @click="addTransaction"
            small
            color="success">
          <v-icon left>mdi-plus</v-icon>
          add
        </v-btn>
      </v-col>

    </v-row>

    <Overlay :overlay="loading"/>

  </div>

</template>

<script>
import Overlay from "@/components/app/Overlay";

export default {
  components: {Overlay},

  data() {
    return {
      spin: false,
      loading: false,
      transactions: [],
      item: {
        text: '',
        value: '',
        access_token: '',
      },
      defaultItem: {
        text: '',
        value: '',
        access_token: '',
      }
    }
  },
  async created() {
    this.loading = true;
    const pathToken = `/callback/channel/info/${this.$route.params.channel}`;
    this.$store.commit('features/setDynamicPath', pathToken);
    await this.$store.dispatch('features/fetchToken');
    this.defaultItem.access_token = this.$store.getters["features/getToken"];

    let encoded = encodeURIComponent(this.defaultItem.access_token);
    const path = `/data/table/?access_token=${encoded}`;
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
      await this.$axios.post('/data/table', this.defaultItem)
          .then((res) => {
            this.transactions.push(res.data);
            this.$notifier.showMessage({
              content: `add data table is successfully`,
              color: 'success'
            })
          })
          .catch((err) => {
            console.error(err);
          })
      this.loading = false;
    },

    async save(item) {
      this.spin = true;
      const path = `/data/table/${item._id}`;
      await this.$axios.put(path, item)
          .then(() => {
            this.$notifier.showMessage({
              content: `updated data table`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `duplicate value | status code ${err.response.status}`,
              color: 'red'
            })
            console.error(err);
          })
      this.spin = false
    },

    async remove(item) {
      this.loading = true;
      const path = `/data/table/${item._id}`;
      await this.$axios.delete(path)
          .then((res) => {
            this.transactions.splice(this.transactions.indexOf(item), 1);
            this.$notifier.showMessage({
              content: `deleted ${item.value}!`,
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
    }
  }

}
</script>

<style scoped>
</style>