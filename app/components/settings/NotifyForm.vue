<template>
  <div>
    <v-row>
      <v-col cols="12"
             sm="6"
             v-for="item in botInfo.forms" :key="item._id">
        <v-form>
          <v-card flat>
            <v-card-title>
              Form Custom
            </v-card-title>

            <v-card-text>

              <v-text-field
                  label="Name"
                  v-model="item.name"
                  hint="form name."
                  persistent-hint
                  readonly
                  filled
              ></v-text-field>

            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                  color="red"
                  text
                  small
                  @click="remove(item)"
              >
                delete
              </v-btn>

              <v-btn
                  color="success"
                  text
                  small
              >
                save
              </v-btn>
            </v-card-actions>

          </v-card>
        </v-form>
      </v-col>

      <v-col cols="12"
             sm="6"
      >
        <v-btn
            small
            color="success"
            class="mx-2"
            fab
            dark
            @click="dialog = true"
        >
          <v-icon>
            mdi-plus
          </v-icon>
        </v-btn>
      </v-col>
    </v-row>


    <v-dialog
        v-model="dialog"
        persistent
        max-width="650px"
    >
      <v-form
          ref="form"
          v-model="valid"
          lazy-validation
      >
        <v-card>
          <v-card-title class="text-h5">
            Select your forms
          </v-card-title>

          <v-card-text>
            <v-container class=" text-center p-2">

              <v-select
                  return-object
                  v-model="form"
                  :items="forms"
                  :rules="[v => !!v || 'Item is required']"
                  label="form"
                  item-text="name"
                  hint="select your form for notify."
                  persistent-hint
                  required
              >
              </v-select>

            </v-container>
          </v-card-text>

          <v-card-actions>

            <v-spacer></v-spacer>
            <v-btn
                class="mr-4"
                color="red"
                text
                @click="dialog = false"
            >
              cancel
            </v-btn>

            <v-btn
                :disabled="!valid"
                class="mr-4"
                color="success"
                text
                :loading="spin"
                @click="add"
            >
              Save
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-form>
    </v-dialog>
  </div>
</template>

<script>

export default {
  props: {
    botInfo: {
      type: Object,
      default: {},
      required: true
    },
    forms: {
      type: Array,
      default: [],
      required: true
    },
    token: {
      type: String,
      default: '',
      required: true
    }
  },

  data() {
    return {
      form: null,
      rules: [v => !!v || 'Required'],
      valid: true,
      spin: false,
      dialog: false,
    }
  },

  methods: {
    async createForm() {
      const path = `/notification/update/webhook/${this.botInfo.token}`
      await this.$axios.put(path, this.botInfo)
          .then((res) => {
            console.log(res.data)
          })
          .catch((err) => {
            console.error(err);
          })
    },

    async api() {
      this.spin = true;
      const path = `/notification/update/webhook/${this.token}?id_form=${this.form ? this.form._id : null}`;
      await this.$axios.put(path, this.botInfo)
          .then((res) => {
            console.log(res.data)
          })
          .catch((err) => {
            console.log(err);
          })
    },

    async createNotification() {
      try {
        let validate = this.$refs.form.validate();
        if (validate) {
          await this.api();
        }
      } catch {
        await this.api();
      }
      this.dialog = false;
      this.spin = false;
    },

    async add() {
      this.botInfo.forms.push(this.form)
      await this.createNotification();
      this.$notifier.showMessage({
        content: `add successfully `,
        color: 'success'
      })
      this.form = null
    },

    async update() {
      await this.createNotification();
      this.$notifier.showMessage({
        content: `updated successfully `,
        color: 'warning'
      })
    },

    async remove(item) {
      let index = this.botInfo.forms.indexOf(item)
      this.botInfo.forms.splice(index, 1)
      await this.createNotification();
      this.$notifier.showMessage({
        content: `deleted successfully `,
        color: 'red'
      })
    }

  },

}

</script>

