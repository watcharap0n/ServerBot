<template>

  <v-container
      class="d-flex justify-center"
  >
    <div class="d-flex flex-column justify-space-between align-center">
      <v-img
          :src="require('~/assets/images/mango-profile.jpg')"
          width="280"
      ></v-img>

      <v-card flat>

        <v-card-text>
          <div v-for="(v, k) in models">

            <div v-if="transaction.models[k]">
              <v-text-field
                  v-if="transaction.models[k].type_field === 'default'"
                  v-model="retrieves[v.value]"
                  color="success"
                  :label="transaction.models[k].text"
                  :outlined="transaction.models[k].outlined"
                  :rounded="transaction.models[k].rounded"
                  :solo="transaction.models[k].solo">
              </v-text-field>
            </div>

            <div v-if="transaction.models[k]">
              <v-select
                  v-if="transaction.models[k].type_field === 'select'"
                  :items="transaction.models[k].items_select"
                  v-model="retrieves[v.value].value"
                  color="success"
                  item-color="success"
                  :outlined="transaction.models[k].outlined"
                  :rounded="transaction.models[k].rounded"
                  :solo="transaction.models[k].solo"
              ></v-select>
            </div>
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
            submit
          </v-btn>

          <v-btn
              small
              color="red"
              dark
          >
            cancel
          </v-btn>
        </v-card-actions>

      </v-card>

    </div>
    <overlay :overlay="overlay"/>
  </v-container>

</template>

<script>
import overlay from "@/components/app/overlay";

export default {
  layout: 'public',

  components: {
    overlay
  },

  data() {
    return {
      overlay: false,
      models: [],
      accesstoken: '',
      transaction: {},
      retrieves: {},
    }
  },

  async created() {
    this.overlay = true;
    await this.getform();
    await this.getdatatable();
    this.overlay = false;
  },

  methods: {
    async getform() {
      const path = `/form/find/${this.$route.params.channel}`
      await this.$axios.get(path)
          .then((res) => {
            this.transaction = res.data;
            this.accesstoken = res.data.access_token;
          })
          .catch((err) => {
            console.error(err);
          })
    },

    async getdatatable() {
      let encoded = encodeuricomponent(this.accesstoken);
      const path = `/data/table/find?access_token=${encoded}&default_field=false`
      await this.$axios.get(path)
          .then((res) => {
            this.models = res.data;
          })
          .catch((err) => {
            console.error(err);
          })
    },
    async save() {
      const path = `/retrieve/create?access_token=${this.accesstoken}`;
      await this.$axios.post(path, this.retrieves)
          .then(() => {
            this.$swal.fire(
                'saved',
                'you clicked the button!',
                'success'
            )
          })
          .catch((err) => {
            this.$notifier.showmessage({
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