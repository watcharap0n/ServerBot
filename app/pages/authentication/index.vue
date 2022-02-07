<template>
  <div>
    <Login/>
  </div>
</template>

<script>
import Login from '../../components/Login'
import Register from '../../components/Register'


export default {
  layout: "empty",
  components: {Login, Register},
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