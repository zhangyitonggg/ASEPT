<template>
  <v-container class="spacing-playground pa-16" fluid>
    <component :is="currentComponent" />
    <v-bottom-navigation app fixed color="primary" v-model="activeBtn" @change="handleNavigateClick">
      <v-btn value="news">
        <span>公告</span>
        <v-icon>mdi-message-alert-outline</v-icon>
      </v-btn>
      <v-btn value="waterbar">
        <span>水吧</span>
        <v-icon>mdi-hand-clap</v-icon>
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
import gpt from '@/components/GptHelp.vue';

export default {
  name: 'HomeView',
  components: {
    news,
    money,
    gpt
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
        case 'gpt':
          return "gpt";
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