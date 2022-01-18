<template>
  <div>
    <form ref="form"
          v-model="valid"

    >
      Sign Up

      <v-text-field
          :rules="userNameRules"
          v-model="userName"
          label="Username"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          :rules="firstNameRules"
          v-model="firstName"
          label="Firstname"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          :rules="lastNameRules"
          v-model="lastName"
          label="Lastname"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          :rules="emailRules"
          v-model="email"
          label="Email"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          v-model="password"
          label="Password"
          filled
          rounded
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required]"
          :type="show ? 'text' : 'password'"
          @click:append="show = !show"
      ></v-text-field>
      <v-text-field
          v-model="confirmPassword"
          label="Confirm Password"
          filled
          rounded
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, passwordConfirmationRule]"
          :type="show1 ? 'text' : 'password'"
          @click:append="show1 = !show1"

      ></v-text-field>
      <v-file-input
          :rules="imageRules"
          v-model="fileImage"
          label="File Image"
          filled
          prepend-icon="mdi-camera"
          accept="image/png, image/jpeg, image/bmp"
      ></v-file-input>
      <v-btn
          rounded
          color="success"
          @click="summitData"
          :loading="spinSubmit"
          :disabled="!valid"
      >Submit
      </v-btn>
    </form>


  </div>
</template>

<script>
export default {
  data() {
    return {
      valid: true,
      userName: '',
      firstName: '',
      lastName: '',
      fullName: '',
      email: '',
      password: '',
      confirmPassword: '',
      show: false,
      show1: false,
      fileImage: null,
      objectData: {},
      rules: {
        required: value => !!value || 'Required.'
      },
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      userNameRules: [
        v => !!v || 'username is required',
      ],
      firstNameRules: [
        v => !!v || 'firstname is required',
      ],
      lastNameRules: [
        v => !!v || 'firstname is required',
      ],
      imageRules: [
        v => !!v || 'image is required',
        value => !value || value.size < 2000000 || 'image size 2MB!'
      ],
      spinSubmit: false,
    }
  },
  methods: {
    async summitData() {
      let validation = this.$refs.form.validate()
      if (validation === true) {
        this.spinSubmit = true
        const path = 'http://localhost:8500/authentication/register';
        let formData = new FormData();
        formData.append('file', this.fileImage)
        formData.append('email', this.email)
        formData.append('hashed_password', this.password)
        formData.append('username', this.userName)
        formData.append('full_name', this.firstName + " " + this.lastName)
        await this.API(path, formData)
        this.spinSubmit = false
      }
    },
    async API(path, formData) {
      await this.$axios.post(path, formData)
          .then((res) => {
            console.log(res.data)
            this.$refs.form.reset()
            this.$swal.fire({
              position: 'top-end',
              icon: 'success',
              title: 'SignIn Success',
              showConfirmButton: false,
              timer: 1500
            })
          })
          .catch((err) => {
            console.error(err)
            this.$refs.form.reset()
            this.$swal.fire({
              icon: 'error',
              title: 'incomplete information',
              text: 'Data invalid',
              footer: '<a href="">Why do I have this issue?</a>'
            })
          })
    }
  },
  computed: {
    passwordConfirmationRule() {
      return () => (this.password === this.confirmPassword) || 'Password must match'
    }
  }
}
</script>

<style scoped>
</style>