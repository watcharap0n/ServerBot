<template>
  <v-card class="text-center p-2" flat>
    <v-card-text>
      <v-form ref="formCard"
              v-model="valid">
        <p class="text-l font-normal  ">Name</p>
        <v-text-field
            rounded
            color="red"
            prepend-icon="mdi-card-text"
            v-model="card.name"
            label="input name"
            filled
        ></v-text-field>
        <p class="text-l font-normal  ">Code</p>
        <v-textarea
            rounded
            filled
            color="red"
            prepend-icon="mdi-code-braces"
            v-model="card.content"
            label="code"
        >
        </v-textarea>

        <p class="text-l font-normal  ">Description</p>
        <v-text-field
            rounded
            filled
            color="red"
            prepend-icon="mdi-message-bulleted"
            v-model="card.message"
            label="input description"
        ></v-text-field>
        <v-row justify="center">
          <p class="text-center  text-red-400">*You can go to design a flex message at:</p> &nbsp;&nbsp;&nbsp;
          <a class="text-center text-base" href="https://developers.line.biz/flex-simulator/" target="_blank">
            Flex Message
          </a>
        </v-row>
        <v-row justify="end">
          <v-btn
              text
              color="info"
              :loading="!spin"
              @click="updateCard"
          >
            <v-icon left>mdi-database-plus</v-icon>
            Save
          </v-btn>
          <v-btn
              :loading="!spin"
              color="grey"
              dark
              @click="deleteCard"
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
    deleteCard: {
      required: false
    },
    updateCard: {
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
    }
  },
  computed: {
    card: {
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