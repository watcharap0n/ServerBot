<template>
  <v-card>

    <v-card-title>
      <v-icon
          color="info"
          class="p-2"
      >
        mdi-account-box-outline
      </v-icon>
      Basic Information
    </v-card-title>

    <v-card-text>
      <v-card
          class="mb-6"
          flat
          tile
      >
        <v-card
            class="pa-2 align-self-stretch text-center"
            flat
        >

          <v-avatar
              class="profile"
              color="grey"
              size="120"
              tile
          >
            <img
                :src="!imgFile ? $auth.user.img_path : urlAvatar"
                @error="setFallbackImageUrl"
            >
          </v-avatar>

        </v-card>

        <v-card
            class="pa-2 align-self-start m-3"
            flat
        >

          <v-text-field
              prepend-inner-icon="mdi-account-outline"
              small
              label="Display name"
              v-model="profile.username"
          >
          </v-text-field>

          <v-text-field
              prepend-inner-icon="mdi-account-circle-outline"
              v-model="profile.full_name"
              small
              label="Full name"
          >
          </v-text-field>

          <v-file-input
              @change="previewImage"
              v-model="imgFile"
              :rules="rulesImg"
              placeholder="Pick an avatar"
              accept="image/png, image/jpeg"
              prepend-icon="mdi-camera"
              truncate-length="25"
              chips
              show-size
              label="Avatar"
          >

          </v-file-input>

          <v-text-field
              disabled
              prepend-inner-icon="mdi-email-outline"
              v-model="$auth.user.email"
              small
              label="Email"
          >
          </v-text-field>

          <v-text-field
              v-model="profile.phone_number"
              small
          >
            <template v-slot:label>
              <div>
                Phone number
                <small>
                  (optional)
                </small>
              </div>
            </template>
          </v-text-field>

          <div class="p-1">
            <small class="text-gray-400">
              UID: {{ $auth.user.uid }}
            </small>
            <v-icon
                small
                @click="copyUID"
            >
              mdi-content-copy
            </v-icon>
          </div>

          <v-checkbox
              hide-details
              disabled
              v-model="$auth.user.disabled"
          >
            <template v-slot:label>
              <div>
                Email
                <v-tooltip bottom>
                  <template v-slot:activator="{ on }">
                    <a
                        target="_blank"
                        href="https://vuetifyjs.com"
                        @click.stop
                        v-on="on"
                    >
                      Verified
                    </a>
                  </template>
                </v-tooltip>
              </div>
            </template>
          </v-checkbox>

        </v-card>
      </v-card>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
          @click="updateProfile"
          color="success"
          disabled
      >
        Save
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      rulesImg: [
        value => !value || value.size < 1000000 || 'Avatar size should be less than 1 MB!',
      ],
      profile: {},
      urlAvatar: null,
      imgFile: null,
      displayName: '',
      fullName: '',
      phoneNumber: '',
    }
  },

  async created() {
    await this.getProfile();
  },

  methods: {
    setFallbackImageUrl(event) {
      event.target.src = require(`~/assets/images/mango-profile.jpg`)
    },

    previewImage() {
      if (this.imgFile)
        this.urlAvatar = URL.createObjectURL(this.imgFile);
    },

    copyUID() {
      this.$copyText(this.$auth.user.uid)
          .then(() => {
            this.$notifier.showMessage({
              content: 'is copied.',
              color: 'info'
            })
          })
    },

    async getProfile() {
      const path = '/authentication/user';
      await this.$axios.get(path)
          .then((res) => {
            console.log(res.data)
            this.profile = res.data.data
          })
          .catch((err) => {
            console.error(err);
          })
    },

    async updateProfile() {
      const path = '/authentication/settings/profile';
      let formData = new FormData();
      formData.append('file', this.imgFile);
      formData.append('display_name', this.displayName);
      formData.append('full_name', this.fullName);
      formData.append('phone_number', this.phoneNumber);
      await this.$axios.post(path, formData)
          .then((res) => {
            this.$notifier.showMessage({
              content: `${res.data}`,
              color: 'success'
            })
          })
          .catch((err) => {
            console.error(err)
            this.$notifier.showMessage({
              content: `${err.response.data}`,
              color: 'red'
            })
          })
    }
  }
}

</script>