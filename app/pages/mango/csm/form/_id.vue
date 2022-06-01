<template>

  <v-form class="h-auto">
    <v-card flat
            color="grey lighten-5"
            class="justify-space-between align-center">
      <v-card-actions>
        <v-btn
            fab
            small
            color="secondary"
            class="text-decoration-none"
            to="/mango/csm/home"
        >
          <v-icon>mdi-arrow-u-left-top</v-icon>
        </v-btn>
        <v-subheader class="text-h6">ข้อมูลการติดต่อ</v-subheader>
      </v-card-actions>

      <v-card flat>
        <v-card-text>
          <v-row>
            <v-col
                cols="4"
                sm="4"
            >
              <v-select
                  :items="address"
                  hint="บ้านเลขที่"
                  placeholder="55/12"
                  persistent-hint
                  dense
              ></v-select>
            </v-col>

            <v-col cols="8" sm="8">
              <v-text-field
                  outlined
                  rounded
                  placeholder="แมงโก้ สีเขียว"
                  hint="ลูกค้า (เจ้าของบ้าน)"
                  persistent-hint
                  dense
              ></v-text-field>
            </v-col>
          </v-row>
          <v-subheader>ชื่อผู้แจ้งซ่อม</v-subheader>

          <v-row style="margin-top: -35px">
            <v-col
                cols="6"
                sm="6"
            >
              <v-checkbox
                  v-model="checkout"
              >
                <template v-slot:label>
                  <small>ลูกค้าเป็นผู้แจ้งเรื่อง</small>
                </template>
              </v-checkbox>
            </v-col>
            <v-col
                cols="6"
                sm="6"
                style="margin-top: 20px"
            >
              <div>เบอร์โทรศัพท์</div>
            </v-col>
          </v-row>

          <v-row style="margin-top: -40px">
            <v-col cols="7" sm="7">
              <v-text-field
                  outlined
                  rounded
                  placeholder="ระบุชื่อผู้แจ้งซ่อม"
                  hint="ระบุชื่อผู้แจ้งซ่อม"
                  persistent-hint
                  dense
              ></v-text-field>
            </v-col>

            <v-col cols="5" sm="5">
              <v-text-field
                  outlined
                  rounded
                  placeholder="0941499661"
                  hint="เบอร์ติดต่อ"
                  persistent-hint
                  dense
              ></v-text-field>
            </v-col>
          </v-row>

          <v-subheader> วันที่สะดวกให้เจ้าหน้าที่เข้าไปตรวจสอบ</v-subheader>

          <v-row>
            <v-col cols="6" sm="6">
              <v-menu
                  v-model="menuDate1"
                  :close-on-content-click="false"
                  max-width="290"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      clearable
                      :value="computedDateFormattedMomentjs"
                      readonly
                      dense
                      v-bind="attrs"
                      v-on="on"
                      @click:clear="date1 = null"
                      hint="วันที่"
                      persistent-hint
                  >
                  </v-text-field>
                </template>
                <v-date-picker
                    locale="th"
                    color="#00BF9D"
                    v-model="date1"
                    @change="menuDate1 = false"
                ></v-date-picker>
              </v-menu>
            </v-col>

            <v-col cols="3" sm="3">
              <v-menu
                  ref="menuStart1"
                  v-model="menuTimeStart1"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="start1"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      v-model="start1"
                      dense
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      hint="เริ่มช่วงเวลา"
                      persistent-hint
                  ></v-text-field>
                </template>
                <v-time-picker
                    color="#00BF9D"
                    v-if="menuTimeStart1"
                    v-model="start1"
                    :max="end1"
                    full-width
                    @click:minute="$refs.menuStart1.save(start1)"
                ></v-time-picker>
              </v-menu>
            </v-col>

            <v-col cols="3" sm="3">
              <v-menu
                  ref="menuEnd1"
                  v-model="menuTimeEnd1"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="end1"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      v-model="end1"
                      dense
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      hint="จบช่วงเวลา"
                      persistent-hint
                  ></v-text-field>
                </template>
                <v-time-picker
                    color="#00BF9D"
                    v-if="menuTimeEnd1"
                    v-model="end1"
                    :min="start1"
                    full-width
                    @click:minute="$refs.menuEnd1.save(end1)"
                ></v-time-picker>
              </v-menu>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="6" sm="6">
              <v-menu
                  v-model="menuDate2"
                  :close-on-content-click="false"
                  max-width="290"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      clearable
                      :value="computedDateFormattedMomentjs"
                      readonly
                      dense
                      v-bind="attrs"
                      v-on="on"
                      @click:clear="date2 = null"
                      hint="วันที่"
                      persistent-hint
                  >
                  </v-text-field>
                </template>
                <v-date-picker
                    locale="th"
                    color="#00BF9D"
                    v-model="date2"
                    @change="menuDate2 = false"
                ></v-date-picker>
              </v-menu>
            </v-col>

            <v-col cols="3" sm="3">
              <v-menu
                  ref="menuStart1"
                  v-model="menuTimeStart2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="start2"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      v-model="start2"
                      dense
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      hint="เริ่มช่วงเวลา"
                      persistent-hint
                  ></v-text-field>
                </template>
                <v-time-picker
                    color="#00BF9D"
                    v-if="menuTimeStart2"
                    v-model="start2"
                    :max="end2"
                    full-width
                    @click:minute="$refs.menuStart1.save(start2)"
                ></v-time-picker>
              </v-menu>
            </v-col>

            <v-col cols="3" sm="3">
              <v-menu
                  ref="menuEnd1"
                  v-model="menuTimeEnd2"
                  :close-on-content-click="false"
                  :nudge-right="40"
                  :return-value.sync="end2"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      v-model="end2"
                      dense
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      hint="จบช่วงเวลา"
                      persistent-hint
                  ></v-text-field>
                </template>
                <v-time-picker
                    color="#00BF9D"
                    v-if="menuTimeEnd2"
                    v-model="end2"
                    :min="start2"
                    full-width
                    @click:minute="$refs.menuEnd1.save(end2)"
                ></v-time-picker>
              </v-menu>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="12">
              <v-text-field
                  outlined
                  rounded
                  dense
                  hint="หมายเหตุ"
                  persistent-hint
              ></v-text-field>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
      <br>

      <v-card flat>
        <v-subheader class="text-h6">รายละเอียดการแจ้งซ่อม</v-subheader>
        <v-card-text>
          <v-text-field
              hint="เรื่อง"
              persistent-hint
              dense
              rounded
              outlined
          ></v-text-field>

          <v-textarea
              hint="รายละเอียด"
              persistent-hint
              dense
              rounded
              outlined
          ></v-textarea>

          <v-file-input
              @change="previewImage"
              v-model="files"
              placeholder="Remark"
              label="File input"
              prepend-icon="mdi-paperclip"
              rounded
              outlined
              dense
              counter
              accept="image/png, image/jpeg"
              :rules="rulesImg"
              :show-size="1000"
          >
            <template v-slot:selection="{ text }">
              <v-chip
                  small
                  label
                  color="primary"
              >
                {{ text }}
              </v-chip>
            </template>
          </v-file-input>

          <img
              v-if="files"
              :src="url"
          >

        </v-card-text>

        <v-btn
            block
            color="#00BF9D"
            dark
        >
          บันทึก
        </v-btn>

      </v-card>
    </v-card>
  </v-form>
</template>

<script>
import moment from 'moment'
import {format, parseISO} from 'date-fns'

export default {
  layout: 'public',
  data() {
    return {
      address: ['55/11', '468', '32/33'],

      checkout: false,
      menuDate1: false,
      menuTimeStart1: false,
      menuTimeEnd1: false,
      date1: format(parseISO(new Date().toISOString()), 'yyyy-MM-dd'),
      start1: null,
      end1: null,

      menuDate2: false,
      menuTimeStart2: false,
      menuTimeEnd2: false,
      date2: format(parseISO(new Date().toISOString()), 'yyyy-MM-dd'),
      start2: null,
      end2: null,

      files: null,
      url: null,
      rulesImg: [
        value => !value || value.size < 1000000 || 'image size should be less than 1 MB!',
      ],
    }
  },

  computed: {
    computedDateFormattedMomentjs() {
      moment.locale('th');
      if (this.date1) {
        return moment(this.date1).format('dd D MMMM YYYY')
      } else if (this.date2) {
        return moment(this.date2).format('dd D MMMM YYYY')
      } else {
        return ''
      }
    }
  },

  methods: {
    previewImage() {
      if (this.files)
        this.url = URL.createObjectURL(this.files);
    },
  }


}
</script>

<style scoped>
</style>