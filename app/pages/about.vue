<template>
  <div>
    <draggable v-model="myArray">
      <transition-group>
        <div v-for="element in myArray" :key="element">
          {{ element }}
        </div>
      </transition-group>
    </draggable>

  </div>
</template>

<script>

export default {
  components: {
    draggable,
  },
  data() {
    return {
      myArray: ['1', '2', '3']
    }
  }
}
</script>

<style scoped>
</style>