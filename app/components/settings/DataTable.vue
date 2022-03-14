<template>

  <v-row>

    <v-col
        v-if="transactions.length > 0"
        v-for="(v, k) in transactions"
        :key="k"
        sm="10">

      <v-card>
        <v-form
            ref="form"
            v-model="valid"
            lazy-validation
        >

          <v-card-text>

            <v-switch
                dense
                v-model="v.status"
                :label="v.status ? 'Enabled': 'Disabled'"
            ></v-switch>

            <v-row>
              <v-col cols="12"
                     sm="6"
              >
                <v-text-field
                    :rules="rules"
                    dense
                    outlined
                    rounded
                    hint="Set your name column, example Name"
                    persistent-hint
                    label="Name Column"
                    v-model="v.text"
                    color="info"
                ></v-text-field>

                <div v-if="v.type_field === 'select'">
                  <v-row>
                    <v-col sm="12">
                      <v-text-field
                          dense
                          rounded
                          outlined
                          v-model="input"
                          hint="add value type select, example name, email, address"
                          persistent-hint
                          @keydown.enter="addSelectValue(v.items_select)"
                      >
                      </v-text-field>
                    </v-col>
                  </v-row>
                </div>
              </v-col>


              <v-col cols="12"
                     sm="6"
              >
                <v-select
                    :filled="!!v.default_field"
                    :readonly="!!v.default_field"
                    :items="items"
                    dense
                    outlined
                    rounded
                    hint="Set your type field for save data, example name"
                    persistent-hint
                    label="Type"
                    v-model="v.type_field"
                    color="info"
                ></v-select>

                <div v-if="v.type_field === 'select'">
                  <v-row>
                    <v-col sm="12">

                      <v-list dense>
                        <v-list-group
                            color="info"
                            :value="true"
                            prepend-icon="mdi-dns-outline"
                        >
                          <template v-slot:activator>
                            <v-list-item-title>Users</v-list-item-title>
                          </template>

                          <v-list-item link v-for="item in v.items_select">
                            <v-list-item-title v-text="item"></v-list-item-title>
                            <v-list-item-icon>
                              <v-btn color="red"
                                     icon
                                     @click="removeItem({item: item, items: v.items_select})"
                              >
                                <v-icon>mdi-close-box-outline</v-icon>
                              </v-btn>
                            </v-list-item-icon>
                          </v-list-item>
                        </v-list-group>
                      </v-list>

                    </v-col>
                  </v-row>
                </div>

              </v-col>

            </v-row>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                :disabled="!!v.default_field"
                @click="remove(v)"
                small
                color="grey">
              Remove
            </v-btn>
            <v-btn
                @click="todo(v)"
                small
                :loading="spin"
                :disabled="!valid"
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

    <Overlay :overlay="loading"/>
  </v-row>

</template>

<script>
import Overlay from "@/components/app/Overlay";

export default {
  components: {Overlay},

  data() {
    return {
      valid: false,
      input: '',
      itemsSelect: [],
      showDetail: true,
      items: ['default', 'select', 'switch'],
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
        type_field: 'default',
        access_token: '',
      },
      rules: [
        v => !!v || 'please enter value',
      ],
    }
  },
  async created() {
    this.loading = true;
    const pathToken = `/callback/channel/info/${this.$route.params.channel}`;
    this.$store.commit('features/setDynamicPath', pathToken);
    await this.$store.dispatch('features/fetchToken');
    this.defaultItem.access_token = this.$store.getters["features/getToken"];

    let encoded = encodeURIComponent(this.defaultItem.access_token);
    const path = `/data/table/find?access_token=${encoded}`;
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
    addSelectValue(value) {
      value.push(this.input)
      this.input = ''
    },

    removeItem(val) {
      let index = val.items.indexOf(val.item)
      val.items.splice(index, 1)
    },

    async addTransaction() {
      this.loading = true;
      await this.$axios.post('/data/table/create', this.defaultItem)
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

    async todo(item) {
      this.spin = true;
      const path = `/data/table/query/update/${item._id}`;
      await this.$axios.put(path, item)
          .then(() => {
            this.$notifier.showMessage({
              content: `updated data table`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `${err.response.data.detail} | status code ${err.response.status}`,
              color: 'red'
            })
            console.error(err);
          })
      this.spin = false
    },

    async remove(item) {
      this.loading = true;
      const path = `/data/table/query/delete/${item._id}`;
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
      this.loading = false;
    }
  }

}
</script>

<style scoped>
</style>