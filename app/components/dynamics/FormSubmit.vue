<template>
  <div>

    <v-form>
      <v-text-field v-model="formEle.ele1"
                    rounded
                    filled
                    :label="nameEle1"
      >
      </v-text-field>

      <v-text-field v-model="formEle.ele2"
                    rounded
                    filled
                    v-if="field1"
                    :label="nameEle2"
      >
      </v-text-field>
      <v-btn color="pink accent-2"
             rounded
             v-text="nameBtn"
             @click="submitForm(formEle)"
             class="text-white"
      >

      </v-btn>
    </v-form>
  </div>
</template>

<script>
export default {
  props: [
    'submitForm',
    'nameBtn',
    'field1',
    'nameEle1',
    'nameEle2',
  ],
  data() {
    return {
      formEle: {
        ele1: '',
        ele2: '',
      },
    }
  }
}
</script>

<style scoped>
</style>