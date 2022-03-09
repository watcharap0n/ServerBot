<template>
  <v-card class="text-center p-2" flat>
    <v-card-text>

      <p class="text-xl font-normal font-extrabold ">Name</p>
      <v-text-field
          v-model="image.name"
          prepend-icon="mdi-card-text"
          rounded
          filled
      ></v-text-field>
      <div v-if="image.size">
        <v-row>
          <v-col
              cols="12" sm="6">
            <p class="text-l font-normal font-bold ">Width</p>
            <v-text-field
                v-if="image.size"
                v-model="image.size.width"
                label="width"
                outlined
                rounded
            ></v-text-field>
          </v-col>
          <v-col
              cols="12" sm="6">
            <p class="text-l font-normal font-bold ">Height</p>
            <v-text-field
                outlined
                rounded
                v-if="image.size"
                v-model="image.size.height"
                label="height"
            ></v-text-field>
          </v-col>
        </v-row>
      </div>
      <div v-if="image.content">
        <p class="text-xl font-normal font-extrabold ">Code</p>
        <v-textarea
            rounded
            filled
            color="red"
            prepend-icon="mdi-code-braces"
            v-model="image.content"
            label="code"
        >
        </v-textarea>
        <v-row justify="end">
          <v-btn
              color="info"
              rounded
              @click="showDetail = !showDetail"
          >Show detail
          </v-btn>
        </v-row>
      </div>

      <div v-if="!image.content">
        <p class="text-xl font-normal font-extrabold ">Code</p>
        <v-textarea
            rounded
            filled
            color="red"
            prepend-icon="mdi-code-braces"
            v-model="content"
            label="code"
        >
        </v-textarea>
        <v-row justify="end">
          <v-btn
              color="success"
              :loading="!spin"
              rounded
          >add content

          </v-btn>
        </v-row>

      </div>


      <div
          v-if="image.content"
          :hidden="!showDetail">
        <v-col
            v-if="image.areas"
            v-for="(v, k) in image.areas"
            :key="k"

        ><span>Mapping</span> {{ k + 1 }}

          <v-card
              class="d-flex justify-space-around mb-4 "
              :color="$vuetify.theme.dark ? 'grey darken-3' : 'grey lighten-4'"
              tile
          >
            <v-card-text>
              <v-row>

                <v-col sm="3">
                  <v-text-field
                      v-model="v.bounds.x"
                      label="X"
                      outlined
                      readonly
                  ></v-text-field>
                </v-col>

                <v-col sm="3">
                  <v-text-field
                      v-model="v.bounds.y"
                      label="Y"
                      outlined
                      readonly
                  ></v-text-field>
                </v-col>

                <v-col sm="3">
                  <v-text-field
                      v-model="v.bounds.width"
                      label="WIDTH"
                      outlined
                      readonly
                  ></v-text-field>
                </v-col>

                <v-col sm="3">
                  <v-text-field
                      v-model="v.bounds.height"
                      label="HEIGHT"
                      outlined
                      readonly
                  ></v-text-field>
                </v-col>

              </v-row>

              <v-text-field
                  v-model="v.action.type"
                  label="type"
                  outlined
                  readonly
              ></v-text-field>

              <div
                  v-if="v.action.type === 'message'"
              >
                <v-text-field
                    v-model="v.action.text"
                    label="data"
                    outlined
                    readonly
                ></v-text-field>
              </div>

              <div
                  v-if="v.action.type === 'uri'"
              >
                <v-text-field
                    v-model="v.action.uri"
                    label="data"
                    outlined
                    readonly
                ></v-text-field>
              </div>
            </v-card-text>

          </v-card>
        </v-col>
      </div>

      <p class="text-xl font-normal font-extrabold ">Description</p>
      <v-text-field
          rounded
          filled
          color="red"
          prepend-icon="mdi-message-bulleted"
          v-model="image.description"
          label="description"
      ></v-text-field>

      <v-row justify="end">
        <v-btn
            text
            color="info"
            :loading="!spinSave"
            @click="todo"
        >
          <v-icon left>mdi-database-plus</v-icon>
          Save
        </v-btn>

        <v-btn
            color="grey"
            dark
            @click="dialog = true"
            text
        >
          <v-icon left>mdi-delete</v-icon>
          delete
        </v-btn>
      </v-row>

    </v-card-text>
    <Dialog :dialog.sync="dialog"
            header="delete Image"
            body="are you sure to delete ?"
            max-width="350"
            :loading-dialog="!spin"
            :submit-dialog="remove"
    />
  </v-card>
</template>

<script>
import Dialog from "@/components/app/Dialog";

export default {
  components: {Dialog},
  props: {
    image: {
      required: false,
      type: Object
    },
    users: {
      required: false
    }

  },
  data() {
    return {
      spinSave: true,
      valid: true,
      showDetail: false,
      content: '',
      dialog: false,
      spin: true

    }
  },

  methods: {

    async todo() {
      this.spinSave = false
      const path = `/mapping/query/update/${this.image.id}`;
      if (this.content)
        this.image.content = this.content
      await this.$axios.put(path, this.image)
          .then((res) => {
            this.$notifier.showMessage({
              content: `updated!`,
              color: 'success'
            })
            console.log(res)
            this.image.areas = res.data.areas
            this.image.size = res.data.size
          })
          .catch((err) => {
            this.$notifier.showMessage({
              content: `something wrong status code ${err.response.status}`,
              color: 'red'
            })
          })
      this.spinSave = true
    },

    async remove() {
      this.spin = false
      const path = `/mapping/query/delete/${this.image._id}`
      this.$store.commit('features/setDynamicPath', path)
      await this.$store.dispatch('features/deleteItem')
      this.users.splice(this.users.indexOf(this.image), 1)
      this.spinSave = true
      this.dialogDelete = false
      this.$notifier.showMessage({
        content: `deleted!`,
        color: 'success'
      })
    },
  }
}
</script>

<style scoped>
</style>