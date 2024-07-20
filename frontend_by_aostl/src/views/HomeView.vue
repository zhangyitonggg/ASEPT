<template>
  <v-container
    class="spacing-playground pa-6"
    fluid
  >
    <news></news>
    <v-footer height="0">
      <v-bottom-navigation
        app
        fixed
        color="primary"
        v-model="activeBtn"
        @change="handleNavigateClick"
      >
        <v-btn value="news">
          <span>公告</span>
          <v-icon>mdi-message-alert-outline</v-icon>
        </v-btn>
        <v-btn value="waterbar">
          <span>水吧</span>
          <v-icon>mdi-hand-clap</v-icon>
        </v-btn>
        <v-btn value="feedback">
          <span>意见</span>
          <v-icon>mdi-invoice</v-icon>
        </v-btn>
      </v-bottom-navigation>
    </v-footer>
  </v-container>
</template>

<script>
import news from '../components/NewsList.vue'

export default {
  name: 'HomeView',
  components: {
    news
  },
  data() {
    return {
      activeBtn: 'news',
    }
  },
  methods: {
    handleNavigateClick(newValue) {
      if (newValue !== 'news') {
        this.$nextTick(() => {
          this.activeBtn = 'news';
          this.$store.commit("setAlert", {"type": "info", "message": "coming soon..."})
        });
      }
    },
  },
  watch: {
  }
}
</script>

<style>
.v-bottom-navigation {
  bottom: 0;
}
</style>