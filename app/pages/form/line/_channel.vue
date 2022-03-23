<template>

  <v-container
      class="d-flex justify-center"
  >
    <div class="d-flex flex-column justify-space-between align-center">
      <v-img
          :src="ImageURI"
          width="280"
      ></v-img>

      <v-card flat>
        <v-card-text>
          <div v-for="(v, k) in models">
            <v-text-field
                v-if="transaction.models[k].type_field === 'default'"
                v-model="retrieves[v]"
                color="success"
                :label="transaction.models[k].text"
                :outlined="transaction.models[k].outlined"
                :rounded="transaction.models[k].rounded"
                :solo="transaction.models[k].solo">
            </v-text-field>

            <v-select
                v-if="transaction.models[k].type_field === 'select'"
                :items="transaction.models[k].items_select"
                v-model="retrieves[v]"
                color="success"
                item-color="success"
                :outlined="transaction.models[k].outlined"
                :rounded="transaction.models[k].rounded"
                :solo="transaction.models[k].solo"
            ></v-select>

          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              small
              color="success"
              dark
              @click="save"
          >
            Submit
          </v-btn>

          <v-btn
              small
              color="red"
              dark
          >
            Cancel
          </v-btn>
        </v-card-actions>

      </v-card>
    </div>
    <Overlay :overlay="overlay"/>
  </v-container>

</template>

<script>
import Overlay from "@/components/app/Overlay";

export default {
  layout: 'public',

  components: {
    Overlay
  },

  data() {
    return {
      overlay: false,
      models: [],
      accessToken: '',
      transaction: {},
      retrieves: {},
    }
  },

  async created() {
    this.overlay = true;
    await this.getForm();
    await this.getDataTable();
    this.overlay = false;
  },

  computed: {
    ImageURI() {
      return require('~/assets/images/mango-profile.jpg')
    }
  },

  methods: {
    async getForm() {
      const path = `/form/find/${this.$route.params.channel}`
      await this.$axios.get(path)
          .then((res) => {
            this.transaction = res.data;
            this.accessToken = res.data.access_token;
          })
          .catch((err) => {
            console.error(err);
          })
    },

    async getDataTable() {
      let encoded = encodeURIComponent(this.accessToken);
      const path = `/data/table/find?access_token=${encoded}&default_field=false`
      await this.$axios.get(path)
          .then((res) => {
            res.data.forEach((item) => {
              this.models.push(item.value)
            })
          })
          .catch((err) => {
            console.error(err);
          })
    },
    async save() {
      const path = `/retrieve/create?access_token=${this.accessToken}`;
      await this.$axios.post(path, this.retrieves)
          .then(() => {
            this.$swal.fire(
                'Saved',
                'You clicked the button!',
                'success'
            )
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `something wrong | status code ${err.response.status}`,
              color: 'red'
            })
          })
    }
  }


}
</script>

<style>

</style>