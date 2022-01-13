<template>

  <v-container>

    <v-row>
      <v-text-field
          v-model="email"
          label="Email"
          solo
      ></v-text-field>
      &nbsp;
      <v-text-field
          v-model="password"
          label="password"
          solo
      ></v-text-field>
    </v-row>

    <v-btn color="success" @click="submitData({'email': email, 'password': password})">
      submit
    </v-btn>

    <br>
    <br>
    <br>
    This is Data - > {{ objectData }}

  </v-container>

</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      objectData: {}
    }
  },
  methods: {
    submitData(val) {
      console.log(val)
      this.objectData = val
    }
  }

}
</script>


<style scoped>

</style>