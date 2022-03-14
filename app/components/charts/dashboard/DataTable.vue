<template>
  <v-data-table
      :headers="headers"
      :items="desserts"
      :loading="loadingTable"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>My Table</v-toolbar-title>
        <v-divider
            class="mx-4"
            inset
            vertical
        ></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="800px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                color="info"
                dark
                v-bind="attrs"
                v-on="on"
            >Add Data
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }} </span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                      v-if="editedItem"
                      cols="12"
                      sm="4"
                      v-for="(value, key) in Object.keys(editedItem)"
                      :key="key"
                      :hidden="!status[key]"
                  >

                    <v-text-field v-if="type_field[key] === 'default'"
                                  v-model="editedItem[value]"
                                  :label="labels[key]">
                    </v-text-field>


                    <v-select
                        v-else-if="type_field[key] === 'select'"
                        v-model="editedItem[value]"
                        :items="itemsSelect[key]"
                        :label="labels[key]">
                    </v-select>

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


    <template v-slot:item.actions="{ item }">
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
    loading: false,
    loadingTable: false,
    access_token: '',
    dialog: false,
    headers: [
      {text: 'Actions', value: 'actions', sortable: false}
    ],
    itemsSelect: [],
    type_field: [],
    status: [],
    labels: [],
    desserts: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {}
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Data' : 'Edit Data'
    }
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
    this.access_token = this.$store.getters["features/getToken"]

    await this.initializeHeader();
  },

  methods: {
    async initializeHeader() {
      this.loadingTable = true;
      let encoded = encodeURIComponent(this.access_token);
      const path = `/data/table/find?access_token=${encoded}&status=${true}`;
      await this.$axios.get(path)
          .then((res) => {
            res.data.forEach((item) => {
              this.headers.push(item);
              this.type_field.push(item.type_field)
              this.labels.push(item.text);
              this.itemsSelect.push(item.items_select)
              this.status.push(item.status);
              this.editedItem[item.value] = null;
              this.defaultItem[item.value] = null;
            })
            this.initializeValue();
          })
          .catch((err) => {
            console.error(err);
          })
      this.loadingTable = false;
    },

    async initializeValue() {
      const path = `/retrieve/?access_token=${this.access_token}`;
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
      const path = `/retrieve/create/?access_token=${this.access_token}`;
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
    }
  }
}
</script>
