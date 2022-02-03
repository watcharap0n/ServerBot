<template>
  <div>
    <Login/>
    <create-chanel/>
  </div>
</template>

<script>
import Login from '../../components/Login'
import Register from '../../components/Register'
import createChanel from "@/components/app/createChanel";

export default {
  layout: "empty",
  components: {Login, Register,createChanel},
  data() {
    return {
      mounted: false,
      title: 'Platform CHATBOT',
      tab: null,
      items: [
        {'header': 'เข้าสู่ระบบ', 'icon': 'mdi-login'},
        {'header': 'สมัครสมาชิก', 'icon': 'mdi-account-plus'}
      ],
    }
  },
  mounted() {
    this.mounted = true
    window.addEventListener('resize', this.wrapperHeight)
    this.wrapperHeight()
  },
  methods: {
    wrapperHeight() {
      if (this.mounted) return
      return this.containerHeight
    }
  }

}
</script>

<style scoped>
</style>