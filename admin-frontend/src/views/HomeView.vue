<template>
  <v-container class="spacing-playground pa-16" fluid>
    <component :is="currentComponent" />
    <v-bottom-navigation app fixed color="primary" v-model="activeBtn" @change="handleNavigateClick">
      <v-btn value="news">
        <span>公告</span>
        <v-icon>mdi-message-alert-outline</v-icon>
      </v-btn>
      <v-btn value="feed">
        <span>反馈</span>
        <v-icon>mdi-chart-box-multiple</v-icon>
      </v-btn>
      <v-btn value="money">
        <span>支持我们</span>
        <v-icon>mdi-hand-coin</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-container>
</template>

<script>
import news from '../components/NewsList.vue'
import money from '../components/GiveMeMoney.vue'
import feed from '../components/FeedBack.vue'

export default {
  name: 'HomeView',
  components: {
    news,
    money,
    feed,
  },
  data() {
    return {
      activeBtn: 'news',
      loading: true,
    }
  },
  computed: {
    currentComponent() {
      switch (this.activeBtn) {
        case 'money':
          return 'money';
        case 'feed':
          return 'feed';
        default:
          return 'news';
      }
    }
  },
  methods: {
    handleNavigateClick(newValue) {
      if (newValue == 'waterbar') {
        this.$nextTick(() => {
          this.activeBtn = 'news';
          this.$store.commit("setAlert", { "type": "info", "message": "coming soon..." })
        });
      }
    },
  },
  watch: {
  }
}
</script>

<style scoped>
.v-bottom-navigation {
  bottom: 0;
}
</style>