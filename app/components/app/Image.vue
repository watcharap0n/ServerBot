<template>
  <v-card class="text-center p-2" flat>
    <v-card-text>
      <v-form ref="formImage"
              v-model="valid">
        <p>Name</p>
        <v-text-field
            v-model="image.name"
            label="name"
            solo
          ></v-text-field>
        <v-row justify="center">
          <p>Width</p>
          <v-text-field
              v-if="image.size"
              v-model="image.size.width"
              label="width"
              solo
          ></v-text-field>
          <p>Height</p>
          <v-text-field
              v-if="image.size"
              v-model="image.size.height"
              label="height"
              solo
          ></v-text-field>
        </v-row>
        <v-textarea
            rounded
            filled
            color="red"
            prepend-icon="mdi-code-braces"
            v-model="image.content"
            label="code"
        >
        </v-textarea>
        <p class="text-xl font-normal font-extrabold ">Code</p>

        <p class="text-xl font-normal font-extrabold ">Description</p>
        <v-text-field
            rounded
            filled
            color="red"
            prepend-icon="mdi-message-bulleted"
            v-model="image.destination"
            label="description"
        ></v-text-field>

        <v-row justify="end">
          <v-btn
              text
              color="info"
              :loading="!spin"
              @click="updateImage"
          >
            <v-icon left>mdi-database-plus</v-icon>
            Save
          </v-btn>
          <v-btn
              :loading="!spin"
              color="grey"
              dark
              @click="deleteImage"
              text
          >
            <v-icon left>mdi-delete</v-icon>
            delete
          </v-btn>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>

export default {
  props: {
    deleteImage: {
      required: false
    },
    updateImage: {
      required: false
    },
    setObject: {
      required: false,
    },
    spin: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      valid: true,
      show: false,
    }
  },
  computed: {
    image: {
      get() {
        return this.setObject;
      },
      set(val) {
        return this.$emit('input', val)
      }
    }
  }
}
</script>

<style scoped>
</style>