<template>
  <v-dialog v-model="dialog" persistent :max-width="maxWidth">
    <v-card>
      <v-toolbar
          flat
          :color="colorToolbar"
          dark
      >
        {{ header }}
      </v-toolbar>
      <v-card-text>
        <div class="p-6">
          <div v-if="body" v-text="body"></div>
          <v-form v-if="elementForms" ref="form" class="p-2">
            <v-text-field
                v-for="(v, k) in elementForms"
                v-model="v.value"
                :key="k"
                :color="v.color"
                :label="v.label"
                :rules="v.rules"
                filled
                :prepend-icon="v.icon ? v.icon : ''"
                rounded
                required
            ></v-text-field>
          </v-form>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red darken-1" text @click="close">cancel</v-btn>
        <v-btn v-if="submitDialog" color="green" :loading="loadingDialog" text @click="submitDialog">save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    loadingDialog: {
      default: false,
      required: false,
    },
    header: {
      default: 'header',
      type: String,
      required: false
    },
    body: {
      type: String,
      required: false
    },
    elementForms: {
      required: false
    },
    submitDialog: {
      required: false,
    },
    dialog: {
      type: Boolean,
      default: false,
    },
    maxWidth: {
      type: String,
      default: '290'
    },
    colorToolbar: {
      type: String,
      default: 'info'
    }
  },
  data() {
    return {}
  },
  methods: {
    close() {
      this.$emit('update:dialog', false)
      try {
        this.$refs.form.reset()
      } catch {

      }
    }
  }
}
</script>

<style scoped>
</style>