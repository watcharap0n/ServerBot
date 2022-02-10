<template>
  <div>
    <v-container>
      <v-col sm="7">
        <v-card class="text-center p-2">

          <v-form ref="formCard"
                  v-model="valid">
            <p class="text-xl font-normal">ชื่อการ์ด</p>
            <v-text-field
                v-model="card.card"
                label="ชื่อการ์ด"
                filled
            ></v-text-field>
            <br>
            <v-divider class="mx-4"></v-divider>
            <br>
            <p class="text-xl font-normal">โค้ด</p>
            <v-textarea
                v-model="card.content"
                label="โค้ด"
            >
              <template>
                <div>
                  โค้ด <small></small>
                </div>
              </template>
            </v-textarea>
            <br>
            <v-divider class="mx-4"></v-divider>
            <br>
            <p class="text-xl font-normal">ข้อความ</p>
            <v-text-field
                v-model="card.massage"
                label="ข้อความ"
                outlined
            ></v-text-field>
            <v-row justify="center">
              <p class="text-center">คุณสามารถไปออกแบบ Card ได้ที่ :</p>
              <a class="text-center" href="https://developers.line.biz/flex-simulator/">
                Card
              </a>
            </v-row>
            <br>
            <v-row justify="end">
              <v-col sm="5">
              <v-btn
                  text
                  x-large
              >บันทึกข้อมูล
              </v-btn>
              <v-btn
                  color="red"
                  fab
                  dark
                  small
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
                </v-col>
            </v-row>

          </v-form>

        </v-card>
      </v-col>
    </v-container>
  </div>
</template>

<script>

export default {
  data() {
    return {
      valid: true,
      card: {
        content: "",
        card: "",
        massage: "",
        accessToken: ""
      }


    }
  }

}
</script>

<style scoped>
</style>