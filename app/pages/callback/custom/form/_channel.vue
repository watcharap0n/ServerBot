<template>
  <div>
    <v-app-bar
        color="info"
        dense
        dark
    >

      <v-toolbar-title>Form Custom</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-btn
          :loading="spinSave"
          @click="todoForm"
          text
          dark
      >
        <v-icon>
          mdi-content-save
        </v-icon>
        Complete
      </v-btn>

      <v-btn
          text
          class="text-decoration-none"
          :to="`/form/LINE/${this.$route.query.q}`"
      >
        <v-icon>
          mdi-arrow-u-right-top
        </v-icon>
        FORM URI
      </v-btn>
    </v-app-bar>

    <v-card
        class="mb-12"
        flat
    >
      <v-card-text v-if="transaction && dataTable">

        <v-row>
          <v-col
              sm="6"
              cols="12"
          >

            <v-card flat>
              <v-card-text>

                <v-card-text>

                  <v-text-field
                      label="ID FORM"
                      color="pink accent-1"
                      v-model="transaction.id_form"
                      hint="id form *(facebook, line)"
                      persistent-hint
                      outlined
                      rounded
                  ></v-text-field>

                </v-card-text>

                <v-divider></v-divider>
                <v-subheader class="d-flex justify-center">
                  Form Data
                </v-subheader>

                <v-combobox
                    v-model="transaction.models"
                    :items="dataTable"
                    item-color="warning"
                    label="choose the data tables"
                    multiple
                    chips
                    color="warning"
                >
                </v-combobox>

                <v-row
                    align="center"
                    v-for="(item, index) in transaction.models"
                    v-if="!item.default_field"
                    :key="index"
                >
                  <v-col
                      cols="8"
                      sm="8">
                    <v-row>

                      <v-text-field
                          v-if="item.type_field === 'default'"
                          color="blue lighten-2"
                          v-model="item.text"
                          hint="type field *default"
                          persistent-hint
                          :outlined="item.outlined"
                          :rounded="item.rounded"
                          :solo="item.solo"
                      ></v-text-field>

                      <v-select
                          v-if="item.type_field === 'select'"
                          :items="item.items_select"
                          v-model="item.selected"
                          color="success"
                          item-color="success"
                          hint="form render form type *select"
                          :solo="item.solo"
                          :rounded="item.rounded"
                          :outlined="item.outlined"
                      ></v-select>
                    </v-row>
                  </v-col>


                  <v-col cols="4" sm="4">
                    <v-card>
                      <v-card-text>

                        <v-checkbox
                            v-model="item.outlined"
                            label="Outlined"
                            hide-details
                            class="shrink mr-3 mt-0"
                            color="red"
                        >
                        </v-checkbox>

                        <v-checkbox
                            v-model="item.solo"
                            label="Solo"
                            hide-details
                            class="shrink mr-3 mt-0"
                            color="red"
                        >
                        </v-checkbox>

                        <v-checkbox
                            v-model="item.rounded"
                            label="Rounded"
                            hide-details
                            class="shrink mr-3 mt-0"
                            color="red"
                        >
                        </v-checkbox>

                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>

              </v-card-text>
            </v-card>
          </v-col>

          <v-col
              sm="6"
              cols="12"
          >
            <v-card>
              <v-card-text>

                <v-subheader class="d-flex justify-center">
                  Created Form
                </v-subheader>
                <v-container
                    v-for="(item, index) in transaction.models"
                    v-if="!item.default_field"
                    :key="index"
                >

                  <v-text-field
                      readonly
                      v-if="item.type_field === 'default'"
                      color="success"
                      :label="item.text"
                      hint="form render type *default"
                      persistent-hint
                      :outlined="item.outlined"
                      :rounded="item.rounded"
                      :solo="item.solo">
                  </v-text-field>

                  <v-select
                      readonly
                      v-if="item.type_field === 'select'"
                      :items="item.items_select"
                      v-model="item.selected"
                      color="success"
                      item-color="success"
                      hint="form render form type *select"
                      :outlined="item.outlined"
                      :rounded="item.rounded"
                      :solo="item.solo"
                  ></v-select>

                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                    small
                    color="success"
                    dark
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
          </v-col>

        </v-row>
      </v-card-text>

    </v-card>

    <Overlay :overlay="overlay"/>

  </div>
</template>

<script>
import Overlay from "@/components/app/Overlay"

export default {

  components: {
    Overlay
  },

  data() {
    return {
      overlay: false,
      spinSave: false,
      rounded: false,
      outlined: false,
      solo: false,
      selectShape: '',
      models: [],
      transaction: null,
      dataTable: null,
    }
  },

  async beforeCreate() {
    await this.$parent.$emit('routerHandle', this.$route.params);
  },

  async created() {
    this.overlay = true;
    await this.getForm();
    await this.getDataTable();
    this.overlay = false;
  },

  methods: {
    async getForm() {
      const path = `/form/find/${this.$route.query.q}`
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
            console.log(res.data)
            this.dataTable = res.data;
          })
          .catch((err) => {
            console.error(err);
          })
    },

    async todoForm() {
      this.spinSave = true
      const path = `/form/query/update/${this.$route.query.q}`
      await this.$axios.put(path, this.transaction)
          .then((res) => {
            this.$notifier.showMessage({
              content: `created form | status code ${res.status}`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `already updated | status code ${err.response.status}`,
              color: 'red'
            })
          })
      this.spinSave = false
    },
  }
}
</script>

<style scoped>
</style>
