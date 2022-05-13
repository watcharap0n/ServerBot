<template>
  <v-card>

    <v-card-title>
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
                :src="$auth.user.img_path"
                @error="setFallbackImageUrl"
            >
          </v-avatar>

          <br>

          <v-btn
              class="m-2"
              text
              small
          >
            Edit Avatar
          </v-btn>
        </v-card>

        <v-card
            class="pa-2 align-self-start m-3"
            flat
        >
          <v-text-field
              small
              label="Display name"
              v-model="$auth.user.username"
          >
          </v-text-field>

          <v-text-field
              v-model="$auth.user.full_name"
              small
              label="Full name"
          >
          </v-text-field>

          <v-text-field
              v-model="$auth.user.email"
              small
              label="Email"
          >
          </v-text-field>

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
          color="info"
      >
        Save
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  data() {
    return {}
  },
  methods: {
    setFallbackImageUrl(event) {
      event.target.src = require(`~/assets/images/mango-profile.jpg`)
    },
  }
}

</script>