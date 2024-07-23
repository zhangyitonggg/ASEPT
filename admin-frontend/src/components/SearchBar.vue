<template>
  <div class="expandable-search">
    <v-btn @click="toggleSearch" v-show="!open ^ this.openBar">
      <v-icon> {{ searchBtnIcon }}</v-icon>
      {{searchBtnText}}
    </v-btn>
      <v-text-field
        v-if="open ^ this.openBar"
        v-model="search"
        @input="updateSearch"
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
    open: false,
    search: '',
  }),
  methods: {
    toggleSearch() {
      this.open = true;
      this.$nextTick(() => {
        this.$refs.searchInput.focus();
      });
    },
    hideSearch() {
      this.search = '';
      this.$emit('input', this.search);
      this.open = false;
    },
    updateSearch() {
      this.$emit('input', this.search);
    },
  },
  props: {
    openBar: {
      type: Boolean,
      default: false,
    },
    searchBtnIcon: {
      type: String,
      default: 'mdi-magnify',
    },
    searchBtnText: {
      type: String,
      default: '搜索',
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
  height: 32px;
}

.v-btn {
  height: 56px; /* Ensuring both have the same height */
}
</style>