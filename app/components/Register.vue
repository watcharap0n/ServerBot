<template>
  <div>
    <v-form ref="formRegister"
            v-model="valid"
    >
      <v-text-field
          color="purple darken-2"
          prepend-inner-icon="mdi-account"
          :rules="userNameRules"
          v-model="userName"
          label="ชื่อผู้ใช้งาน"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          color="purple darken-2"
          prepend-inner-icon="mdi-card-account-details"
          :rules="firstNameRules"
          v-model="firstName"
          label="ชื่อจริง"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          color="purple darken-2"
          prepend-inner-icon="mdi-card-account-details"
          :rules="lastNameRules"
          v-model="lastName"
          label="นามสกุล"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          color="purple darken-2"
          prepend-inner-icon="mdi-email"
          :rules="emailRules"
          v-model="email"
          label="อีเมล"
          filled
          rounded
      ></v-text-field>
      <v-text-field
          color="purple darken-2"
          prepend-inner-icon="mdi-lock"
          v-model="password"
          label="รหัสผ่าน"
          filled
          rounded
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="rules"
          :type="show ? 'text' : 'password'"
          @click:append="show = !show"
      ></v-text-field>
      <v-text-field
          color="purple darken-2"
          prepend-inner-icon="mdi-lock-alert"
          v-model="confirmPassword"
          label="ยืนยันรหัสผ่าน"
          filled
          rounded
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules, passwordConfirmationRule]"
          :type="show1 ? 'text' : 'password'"
          @click:append="show1 = !show1"
      ></v-text-field>
      <v-file-input
          color="purple darken-2"
          :rules="imageRules"
          v-model="fileImage"
          label="รูปภาพ"
          filled
          prepend-icon="mdi-camera"
          accept="image/png, image/jpeg, image/bmp"
      ></v-file-input>
      <v-btn
          class="text-white"
          block
          color="pink accent-2"
          rounded
          @click="summitData"
          :loading="spinSubmit"
          :disabled="!valid"
      >สมัครสมาชิก
      </v-btn>
    </v-form>
  </div>
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
        value => !!value || 'กรุณากรอกรหัสผ่าน',
        v => v && v.length >= 6 || 'กรุณากรอกรหัสผ่านอย่างน้อย 6 ตัว'
      ],
      emailRules: [
        v => !!v || 'กรุณากรอกอีเมล',
      ],
      userNameRules: [
        v => !!v || 'กรุณากรอกชื่อผู้ใช้งาน',
      ],
      firstNameRules: [
        v => !!v || 'กรุณากรอกชื่อจริง',
      ],
      lastNameRules: [
        v => !!v || 'กรุณากรอกนามสกุล',
      ],
      imageRules: [
        value => !!value || 'กรุณาอัพโหลดรูปภาพ',
        value => !value || value.size < 1000000 || 'รูปภาพควรมีขนาด 1MB!'
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
              title: 'สมัครใช้งานสำเร็จ',
              showConfirmButton: false,
              timer: 1500
            }).then(() => {
              this.$emit('update:tabParent', 0)
            })
          })
          .catch((err) => {
            console.log(err.status)
            console.error(err)
            this.$refs.formRegister.reset()
            this.$swal.fire({
              icon: 'error',
              title: 'ผิดพลาด',
              text: 'มีบางอย่างผิดพลาด',
            })
            if (err.response.status === 403) {
              this.$swal.fire({
                icon: 'warning',
                title: 'อีเมลนี้ถูกใช้งานไปแล้ว',
                text: 'กรุณาใช้อีเมลอื่น',

              })
            }
          })
    }

  },
  computed: {
    passwordConfirmationRule() {
      return () => (this.password === this.confirmPassword) || 'โปรดใส่รหัสผ่านให้ถูกต้อง'
    }
  }
}
</script>

<style scoped>
</style>