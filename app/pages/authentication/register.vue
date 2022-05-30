<template>
  <v-container>
    <v-col sm="5" class="text-center">
      <p class="text-center font-bold text-6xl text-green-600">Hello, Friend</p>
      <p class="text-center font-bold text-5xl text-green-600 ">Create Account</p>
      <br>
      <v-form ref="formRegister"
              v-model="valid"
      >
        <v-text-field
            class="border-4 "
            prepend-inner-icon="mdi-account-outline"
            :rules="userNameRules"
            v-model="userName"
            label="Username"
            rounded
        ></v-text-field>
        <br>
        <v-text-field
            class="border-4 "
            prepend-inner-icon="mdi-card-account-details-outline"
            :rules="firstNameRules"
            v-model="firstName"
            label="First Name"
            rounded
        ></v-text-field>
        <br>
        <v-text-field
            class="border-4 "
            prepend-inner-icon="mdi-card-account-details-outline"
            :rules="lastNameRules"
            v-model="lastName"
            label="Last Name"
            rounded
        ></v-text-field>
        <br>
        <v-text-field
            class="border-4 "
            prepend-inner-icon="mdi-at"
            :rules="emailRules"
            v-model="email"
            label="Email"
            rounded
        ></v-text-field>
        <br>
        <v-text-field
            class="border-4 "
            prepend-inner-icon="mdi-lock"
            v-model="password"
            label="Password"
            rounded
            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="rules"
            :type="show ? 'text' : 'password'"
            @click:append="show = !show"
        ></v-text-field>
        <br>
        <v-text-field
            class="border-4 "
            prepend-inner-icon="mdi-lock-alert"
            v-model="confirmPassword"
            label="Confirm Password"
            rounded
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules, passwordConfirmationRule]"
            :type="show1 ? 'text' : 'password'"
            @click:append="show1 = !show1"
        ></v-text-field>
        <br>
        <v-file-input

            :rules="imageRules"
            v-model="fileImage"
            label="Picture"
            prepend-icon="mdi-camera-outline"
            accept="image/png, image/jpeg, image/bmp"
        ></v-file-input>
        <br>
        <v-btn
            x-large
            style="width:200px "
            class="text-white"
            color="teal darken-1"
            rounded
            @click="summitData"
            :loading="spinSubmit"
            :disabled="!valid"
        >Sign Up
        </v-btn>
      </v-form>
    </v-col>
  </v-container>
</template>

<script>
export default {
  layout: "empty",
  props: ['tabParent'],
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
      rules: [
        value => !!value || 'please enter password',
        v => v && v.length >= 6 || 'please enter at least 6 character'
      ],
      emailRules: [
        v => !!v || 'please enter email',
      ],
      userNameRules: [
        v => !!v || 'please enter username',
      ],
      firstNameRules: [
        v => !!v || 'please enter your first name',
      ],
      lastNameRules: [
        v => !!v || 'please enter your last name',
      ],
      imageRules: [
        value => !!value || 'please upload picture',
        value => !value || value.size < 1000000 || 'picture should 1MB!'
      ],
      spinSubmit: false,
    }
  },
  methods: {
    async summitData() {
      let validation = this.$refs.formRegister.validate()
      if (validation === true) {
        this.spinSubmit = true
        const path = '/authentication/register';
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
          .then(() => {
            this.$refs.formRegister.reset()
            this.$swal.fire({
              position: 'top-end',
              icon: 'success',
              title: 'Sign Up success',
              showConfirmButton: false,
              timer: 1500
            }).then(() => {
              this.$router.push('/authentication')
            })
          })
          .catch((err) => {
            console.log(err.status)
            console.error(err)
            this.$refs.formRegister.reset()
            this.$swal.fire({
              icon: 'error',
              title: 'Error',
              text: 'Something wrong!',
            })
            if (err.response.status === 403) {
              this.$swal.fire({
                icon: 'warning',
                title: 'Email already exists',
                text: 'please use another email',

              })
            }
          })
    }

  },
  computed: {
    passwordConfirmationRule() {
      return () => (this.password === this.confirmPassword) || 'please enter a valid password'
    }
  }
}
</script>

<style scoped>
</style>