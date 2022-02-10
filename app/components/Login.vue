<template>
  <div>
    <v-container>
      <v-img
          :fullscreen="$vuetify.breakpoint.mobile"
          position="center"
          max-height="400"
          max-width="250"
          :src="require('~/assets/images/mango-profile.jpg')"
      >

      </v-img>
      <v-col sm="5">
        <p class=" text-7xl font-extrabold text-green-500 " style="color: #00838F">Welcome to</p>
        <p class="text-6xl text-green-500" style="color: #00838F">Platform Chatbot</p>
        <br>
        <br>
        <v-form
            ref="form"
            v-model="valid"
            lazy-validation
        >
          <v-text-field
              style="background-color: #D7F9FA"
              prepend-inner-icon="mdi-account-outline"
              :rules="emailRules"
              v-model="email"
              label="อีเมล"
              rounded
              @keyup.enter="submitLogin"
          >
          </v-text-field>
          <br>
          <v-text-field
              style="background-color: #D7F9FA"
              @click:append="show1 = !show1"
              :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
              :type="show1 ? 'text' : 'password'"
              prepend-inner-icon="mdi-lock"
              :rules="passwordRules"
              v-model="password"
              label="รหัสผ่าน"
              rounded
              @keyup.enter="submitLogin"
          >
          </v-text-field>
          <br>

          <v-row
              align="center"
          >
            <v-col>
              <v-radio-group
                  v-model="radioGroup"
              >
                <v-radio

                    label="จดจำฉัน"
                    color="primary"
                    value="primary"
                ></v-radio>
              </v-radio-group>
            </v-col>

            <v-col sm="4">
              <NuxtLink to="/authentication/forgot" class="text-body">
                ลืมรหัสผ่าน?
              </NuxtLink>
            </v-col>
          </v-row>
          <br>
          <v-btn
              x-large
              style="width:200px"
              color="#12AE7E"
              rounded
              class="text-white "
              @click="submitLogin"
              :loading="spinSubmit"
              :disabled="!valid"
          >เข้าสู่ระบบ
          </v-btn>
          <br>
          <br>
          <br>
          <v-row
              justify="center">
            <p>Don't have an account ?</p>
            <NuxtLink to="/authentication/register"
                      style="color: #3BBBBC"
            >
              สมัครสมาชิก
            </NuxtLink>
          </v-row>
        </v-form>
      </v-col>
    </v-container>

  </div>
</template>

<script>

export default {

  data() {
    return {
      radioGroup: 1,
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
  created() {
    console.log(process.env.branch)
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
          .then(() => {
            // console.log(this.$auth.strategy.token.get())
            this.$router.push('/');
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
  },

}
</script>

<style scoped>
</style>