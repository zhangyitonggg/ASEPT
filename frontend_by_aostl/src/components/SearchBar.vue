<template>
  <div class="expandable-search">
    <v-btn icon @click="toggleSearch" v-show="!showSearch">
      <v-icon style="font-size: 32px;">mdi-magnify</v-icon>
      <span style="font-size:16px;margin-bottom:3%;">&nbsp;搜索</span>
    </v-btn>
      <v-text-field
        v-if="showSearch"
        v-model="search"
        class="search-input"
        dense
        append-icon="mdi-close"
        flat
        hide-details
        @click:append="hideSearch"
        ref="searchInput"
      ></v-text-field>
  </div>
</template>

<script>
export default {
  data: () => ({
    showSearch: false,
    search: '',
  }),
  methods: {
    toggleSearch() {
      this.showSearch = true;
      this.$nextTick(() => {
        this.$refs.searchInput.focus();
      });
    },
    hideSearch() {
      this.search = '';
      this.showSearch = false;
    },
  },
};
</script>

<style scoped>
.expandable-search {
  position: relative; /* Position relative to the parent container */
  display: flex;
  flex-direction: row-reverse; /* Align the button to the right */
}

.search-input {
  width: 250px; /* Define your desired width */
}

</style>