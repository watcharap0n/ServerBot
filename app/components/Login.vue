<template>
  <div>
    <v-form
        ref="form"
        v-model="valid"
        lazy-validation
    >
      <v-text-field
          prepend-inner-icon="mdi-email"
          color="purple darken-2"
          :rules="emailRules"
          v-model="email"
          label="อีเมล"
          filled
          rounded
      >
      </v-text-field>
      <v-text-field
          @click:append="show1 = !show1"
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show1 ? 'text' : 'password'"
          prepend-inner-icon="mdi-lock"
          color="purple darken-2"
          :rules="passwordRules"
          v-model="password"
          label="รหัสผ่าน"
          filled
          rounded
          @keyup.enter="submitLogin"
      >
      </v-text-field>
      <v-btn
          block
          color="pink accent-2"
          rounded
          class="text-white"
          @click="submitLogin"
          :loading="spinSubmit"
          :disabled="!valid"
      >เข้าสู่ระบบ
      </v-btn>
    </v-form>

  </div>
</template>

<script>
export default {
  data() {
    return {
      show1: false,
      valid: true,
      emailRules: [
        v => !!v || 'กรุณากรอกอีเมล',
        v => /.+@.+\..+/.test(v) || 'กรุณากรอกอีเมลให้ถูกต้อง',
      ],
      passwordRules: [
        v => !!v || 'กรุณากรอกรหัสผ่าน',
      ],
      spinSubmit: false,
      email: '',
      password: '',
    }
  },
  methods: {
    async submitLogin() {
      let validation = this.$refs.form.validate();
      if (validation === true) {
        let formData = new FormData();
        formData.append('username', this.email)
        formData.append('password', this.password)
        await this.loginInfo(formData)
      }
    },
    loginInfo(formData) {
      this.spinSubmit = true
      this.$auth.loginWith('local', {data: formData})
          .then((res) => {
            console.log(res);
            this.$router.push('/home');
            this.spinSubmit = false
            this.$refs.form.reset();
          })
          .catch((err) => {
            let response = err.response.status;
            if (response === 403) {
              this.$swal.fire({
                icon: 'warning',
                title: 'กรุณายืนยันตัวตน',
                text: 'กรุณายืนยันตัวตนผ่านอีเมล',
              })
              this.spinSubmit = false
              this.$refs.form.reset();
            } else {
              this.$swal.fire({
                icon: 'error',
                title: 'ผิดพลาด',
                text: 'มีบางอย่างผิดพลาด อีเมลหรือพาสเวิดไม่ถูกต้อง'
              })
              this.spinSubmit = false
              this.$refs.form.reset();
            }
          })
    }
  }
}
</script>

<style scoped>
</style>