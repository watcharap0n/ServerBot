<template>
  <v-data-table
      :headers="headers"
      :items="desserts"
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
                color="primary"
                dark
                v-bind="attrs"
                v-on="on"
            >New Data
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                      cols="12"
                      sm="4"
                      v-for="(value, key) in Object.keys(editedItem)"
                      :key="key"
                  >
                    <v-text-field v-model="editedItem[value]"
                                  :label="labels[key]">
                    </v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
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
          small
          @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
  </v-data-table>
</template>

<script>
export default {
  data: () => ({
    access_token: '',
    dialog: false,
    headers: [
      {text: 'Actions', value: 'actions', sortable: false}
    ],
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

    await this.initialize();
  },

  methods: {
    async initialize() {
      let encoded = encodeURIComponent(this.access_token);
      console.log(encoded)
      const path = `/data/table/?access_token=${encoded}`;
      await this.$axios.get(path)
          .then((res) => {
            res.data.forEach((item) => {
              this.headers.push(item);
              this.labels.push(item.text);
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

    deleteItem(item) {
      const index = this.desserts.indexOf(item);

      confirm('Are you sure you want to delete this item?') && this.desserts.splice(index, 1);
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
        Object.assign(this.desserts[this.editedIndex], this.editedItem);
      } else {
        await this.add();
      }
      this.close()
    },
    async add() {
      const path = `/retrieve/create/?access_token=${this.access_token}`;
      await this.$axios.post(path, this.editedItem)
          .then((res) => {
            this.desserts.push(this.editedItem);
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

    },
    async remove() {

    }
  }
}
</script>
