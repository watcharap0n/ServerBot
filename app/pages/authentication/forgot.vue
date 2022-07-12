<template>
  <div>
    <v-col sm="7">

    <div class="p-28 ">
      <h2 class="text-5xl">
        ลืมรหัสผ่าน
      </h2>
      <br>
      <p>กรอกอีเมลของคุณ และคุณจะได้รับวิธีการเปลี่ยนรหัสผ่านจากเรา</p>

      <FormSubmit name-btn="ลืมรหัสผ่าน"
                  name-ele1="ที่อยู่อีเมล"
                  :submit-form="submitForm"



      />
    </div>

  <v-overlay :value="spinLoading">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>
      </v-col>

  </div>
</template>

<script>
import FormSubmit from "../../components/app/FormSubmit";

export default {
  components: {FormSubmit},
  layout: 'empty',
  data() {
    return {
      spinLoading: false
    }
  },
  methods: {
    async submitForm(infoEle) {
      this.spinLoading = true
      const path = `/authentication/settings/forgot?email=${infoEle.ele1}`
      await this.$axios.get(path)
          .then((res) => {
            console.log(res.data)
            this.$router.push('/authentication')
          })
          .catch((err) => {
            console.error(err)
          })
      this.spinLoading = false
    }
  }
}
</script>

<style scoped>
</style>