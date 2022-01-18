<template>
  <div>
    <v-form
        ref="form"
        v-model="valid"
        lazy-validation
    >
      Sign In
      <p>use your email</p>

      <v-text-field
          :rules="emailRules"
          v-model="email"
          label="Email"
          filled
          rounded
      >
      </v-text-field>
      <v-text-field
          :rules="passwordRules"
          v-model="password"
          label="Password"
          filled
          rounded
      >
      </v-text-field>
      <v-btn
          color="success"
          rounded
          @click="submitLogin"
          :loading="spinSubmit"
          :disabled="!valid"
      >Submit
      </v-btn>
    </v-form>

  </div>
</template>

<script>
export default {
  data() {
    return {
      valid: true,
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      passwordRules: [
        v => !!v || 'Password is required',
      ],
      spinSubmit: false,
      email: '',
      password: '',
      token: ''
    }
  },
  methods: {
    async submitLogin() {
      let validation = this.$refs.form.validate()
      if (validation === true) {
        this.spinSubmit = true
        const path = 'http://localhost:8500/authentication/token';
        let formData = new FormData();
        formData.append('username', this.email)
        formData.append('password', this.password)
        await this.API(path, formData)
        this.spinSubmit = false
      }
    },
    async API(path, formData){
      await this.$axios.post(path, formData)
            .then((res) => {
              console.log(res.data)
              this.token = res.data.access_token
              this.$refs.form.reset()
              this.$swal.fire({
                position: 'top-end',
                icon: 'success',
                title: 'Login Success',
                showConfirmButton: false,
                timer: 1500
              })
            })
            .catch((err) => {
              console.error(err)
              this.$refs.form.reset()
              this.$swal.fire({
                icon: 'error',
                title: 'Not Authenticated',
                text: 'Email or Password invalid',
                footer: '<a href="">Why do I have this issue?</a>'
              })
            })
    }
  }
}
</script>

<style scoped>
</style>