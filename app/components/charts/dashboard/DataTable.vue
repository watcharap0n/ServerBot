<template>
  <v-data-table
      :headers="payloadSelectedHeaders.headers"
      :items="desserts"
      :items-per-page="5"
      :loading="loadingTable"
  >
    <template v-slot:top>
      <v-toolbar flat>

        <v-toolbar-title>Data Table</v-toolbar-title>

        <v-divider
            class="mx-4"
            inset
            vertical
        ></v-divider>


        <v-dialog
            v-model="dialogColumn"
            max-width="500px"
            persistent
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                small
                color="info"
                dark
                depressed
                v-bind="attrs"
                v-on="on"
            >

              <v-icon>
                mdi-view-column-outline
              </v-icon>

            </v-btn>
          </template>

          <v-card>
            <v-toolbar>
              Select Your Columns
            </v-toolbar>

            <br>

            <v-card-text>
              <v-select
                  v-if="payloadSelectedHeaders"
                  v-model="payloadSelectedHeaders.headers"
                  :items="headers"
                  label="Select Columns" multiple outlined
                  return-object
              >
                <template v-slot:selection="{ item, index }">
                  <v-chip v-if="index < 2">
                    <span>{{ item.text }}</span>
                  </v-chip>
                  <span v-if="index === 2" class="grey--text caption">(+{{
                      payloadSelectedHeaders.headers.length - 2
                    }} others)</span>
                </template>
              </v-select>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn
                  @click="dialogColumn = false"
                  text
                  color="grey"
              >
                Cancel
              </v-btn>

              <v-btn
                  @click="saveColumns"
                  :loading="loadingColumn"
                  text
                  color="success"
              >
                Save
              </v-btn>

            </v-card-actions>

          </v-card>
        </v-dialog>

        <v-spacer></v-spacer>

        <v-dialog v-model="dialog" max-width="800px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                color="info"
                dark
                depressed
                v-bind="attrs"
                v-on="on"
            >
              <v-icon left>
                mdi-account-plus-outline
              </v-icon>
              Add
            </v-btn>
          </template>

          <v-card>
            <v-toolbar>
              {{ formTitle }}
            </v-toolbar>

            <br>

            <v-card-text>
              <v-container>

                <v-row
                    v-for="(field, index) in Object.keys(editedItem)"
                    :key="index"
                    v-if="headers"
                >
                  <v-col v-if="!headers[index].default_field">
                    <v-text-field
                        v-if="headers[index].type_field === 'default'"
                        rounded
                        outlined
                        color="info"
                        hint="text field"
                        persistent-hint
                        :label="headers[index].text"
                        v-model="editedItem[field]"
                    ></v-text-field>


                    <v-select
                        rounded
                        outlined
                        hint="select label"
                        persistent-hint
                        v-if="headers[index].type_field === 'select'"
                        :items="headers[index].items_select"
                        :label="headers[index].text"
                        v-model="editedItem[field]"
                        item-color="info"
                    ></v-select>
                  </v-col>
                </v-row>

              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="grey"
                     text
                     @click="close"
                     :loading="loading"
              >
                Cancel
              </v-btn>
              <v-btn color="success"
                     text @click="save"
                     :loading="loading">
                Save
              </v-btn>
            </v-card-actions>

          </v-card>
        </v-dialog>

      </v-toolbar>
    </template>

    <!--    <template v-for="(val, index) in headers"-->
    <!--              v-slot:[`item.${val.value}`]="{ item }"-->
    <!--    >-->
    <!--    </template>-->

    <template v-slot:item.action="{ item }">
      <v-icon
          small
          class="mr-2"
          @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
          :loading="loading"
          small
          @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
  </v-data-table>
</template>

<script>

export default {

  data: () => ({
    loadingColumn: false,
    loading: false,
    loadingTable: false,
    accessToken: '',
    dialog: false,
    dialogColumn: false,
    transactions: [],
    headers: [],
    itemsSelect: [],
    desserts: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {},
    headersMap: {},
    payloadSelectedHeaders: {},
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Data' : 'Edit Data'
    },

  },

  watch: {
    dialog(val) {
      val || this.close()
    }
  },

  async created() {
    const pathToken = `/callback/channel/info/${this.$route.params.channel}`;
    this.$store.commit('features/setDynamicPath', pathToken);
    await this.$store.dispatch('features/fetchToken');
    this.accessToken = this.$store.getters["features/getToken"]
    this.loadingTable = true;
    await this.getSelectedHeaders();
    await this.initializeHeader();
    this.loadingTable = false;
  },

  methods: {
    async initializeHeader() {
      let encoded = encodeURIComponent(this.accessToken);
      const path = `/data/table/find?access_token=${encoded}&status=${true}`;
      await this.$axios.get(path)
          .then((res) => {
            this.headers = res.data;
            res.data.forEach((item) => {
              this.itemsSelect.push(item.items_select)
              this.headersMap[item.value] = item
              this.editedItem[item.value] = null;
              this.defaultItem[item.value] = null;
            })
            this.initializeValue();
          })
          .catch((err) => {
            console.error(err);
          })
    },

    async initializeValue() {
      const path = `/retrieve/find?access_token=${this.accessToken}`;
      await this.$axios.get(path)
          .then((res) => {
            this.desserts = res.data;
          })
          .catch((err) => {
            console.error(err);
          })
    },

    editItem(item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    async deleteItem(item) {
      confirm('Are you sure you want to delete this item?') && await this.remove(item);
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      })
    },

    async save() {
      if (this.editedIndex > -1) {
        this.loading = true;
        await this.todo();
        this.loading = false;
      } else {
        this.loading = true;
        await this.add();
        this.loading = false;
      }
      this.close()
    },

    async add() {
      const path = `/retrieve/create?access_token=${this.accessToken}`;
      await this.$axios.post(path, this.editedItem)
          .then((res) => {
            this.desserts.push(res.data);
            this.$notifier.showMessage({
              content: `add successfully | status code ${res.status}`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `something wrong | status code ${err.response.status}`,
              color: 'red'
            })
          })
    },
    async todo() {
      const path = `/retrieve/query/update/${this.editedItem.id}`
      await this.$axios.put(path, this.editedItem)
          .then((res) => {
            Object.assign(this.desserts[this.editedIndex], this.editedItem);
            this.$notifier.showMessage({
              content: `updated successfully | status code ${res.status}`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `something wrong | status code ${err.response.status}`,
              color: 'red'
            })
          })
    },

    async remove(item) {
      this.loading = true;
      const path = `/retrieve/query/delete/${item.id}`
      await this.$axios.delete(path)
          .then((res) => {
            let index = this.desserts.indexOf(item)
            this.desserts.splice(index, 1);
            this.$notifier.showMessage({
              content: `deleted successfully | status code ${res.status}`,
              color: 'success'
            })
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `something wrong | status code ${err.response.status}`,
              color: 'red'
            })
          })
      this.loading = false;
    },

    async getSelectedHeaders() {
      let encoded = encodeURIComponent(this.accessToken);
      const path = `/data/table/columns/find?access_token=${encoded}&uid=${this.$auth.user.uid}`;
      await this.$axios.get(path)
          .then((res) => {
            this.payloadSelectedHeaders = res.data;
          })
          .catch((err) => {
            console.log(err);
          })
    },

    async saveColumns() {
      this.loadingColumn = true;
      const path = `/data/table/columns/query/update/${this.payloadSelectedHeaders._id}`
      await this.$axios.put(path, {headers: this.payloadSelectedHeaders.headers})
          .then((res) => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err);
          })
      this.dialogColumn = false;
      this.dialogColumn = false;
    }

  }
}
</script>
