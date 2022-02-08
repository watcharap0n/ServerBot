<template>
  <div>

    <v-card>
      <v-toolbar
          color="primary"
          dark
          flat
      >
        <v-icon>mdi-silverware</v-icon>
        <v-toolbar-title>Local hotspots</v-toolbar-title>
      </v-toolbar>

      <v-row>
        <v-col>
          <v-card-text>
            <v-treeview
                v-model="tree"
                :load-children="fetch"
                :items="items"
                selected-color="indigo"
                open-on-click
                selectable
                return-object
                expand-icon="mdi-chevron-down"
                on-icon="mdi-bookmark"
                off-icon="mdi-bookmark-outline"
                indeterminate-icon="mdi-bookmark-minus"
            >
            </v-treeview>
          </v-card-text>
        </v-col>
      </v-row>


    </v-card>

  </div>
</template>

<script>
export default {
  data() {
    return {
      breweries: [],
      isLoading: false,
      tree: [],
      types: [],
    }
  },
  computed: {
    items() {
      const children = this.types.map(type => ({
        id: type,
        name: this.getName(type),
        children: this.getChildren(type),
      }))

      return [{
        id: 1,
        name: 'All Breweries',
        children,
      }]
    },
    shouldShowTree() {
      return this.breweries.length > 0 && !this.isLoading
    },
  },
  watch: {
    breweries(val) {
      this.types = val.reduce((acc, cur) => {
        const type = cur.brewery_type

        if (!acc.includes(type)) acc.push(type)

        return acc
      }, []).sort()
    },
  },
  methods: {
    fetch() {
      if (this.breweries.length) return

      return fetch('https://api.openbrewerydb.org/breweries')
          .then(res => res.json())
          .then(data => (this.breweries = data))
          .catch(err => console.log(err))
    },
    getChildren(type) {
      const breweries = []

      for (const brewery of this.breweries) {
        if (brewery.brewery_type !== type) continue

        breweries.push({
          ...brewery,
          name: this.getName(brewery.name),
        })
      }

      return breweries.sort((a, b) => {
        return a.name > b.name ? 1 : -1
      })
    },
    getName(name) {
      return `${name.charAt(0).toUpperCase()}${name.slice(1)}`
    },
  },

}
</script>

<style scoped>
</style>