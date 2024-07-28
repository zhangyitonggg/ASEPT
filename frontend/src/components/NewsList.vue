<template>
  <div>
    <v-container fluid class="d-flex justify-center align-center" v-if="loading">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-container>
    <v-expansion-panels v-else inset v-model="activePanel" focusable>
      <v-expansion-panel v-if="news.length > 0" v-for="(item, index) in news" :key="index" :value="index === 0"
        :readonly="!item.is_active">
        <v-expansion-panel-header :disable-icon-rotate="!item.is_active">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div>{{ item.title }}</div>
            <div style="color: grey; text-align: right; margin-right: 16px;">
              <span>{{ item.author }}</span>
              <span> - </span>
              <span>{{ formatDate(item.update_at) }}</span>
            </div>
          </div>
          <template v-slot:actions>
            <v-icon :color="item.is_active ? 'primary' : 'error'">
              {{ item.is_active ? '$expand' : 'mdi-alert-circle' }}
            </v-icon>
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div class="panel-content">
            <v-md-preview :text="item.content"></v-md-preview>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-banner v-if="news.length === 0">
        好吧，看起来现在还没有公告。
      </v-banner>
    </v-expansion-panels>
  </div>
</template>

<script>
import { format } from 'date-fns';

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

export default {
  name: "NewsList",
  components: {
    VMdPreview
  },
  data() {
    return {
      news: null,
      loading: true,
      activePanel: 0,
    }
  },
  mounted() {
    this.$store.commit("setAppTitle", "公告");
    this.$store.dispatch("getNews")
      .then(res => {
        this.news = res.announcements;
      })
      .catch(_ => {
        this.news = [];
        this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
      })
      .finally(() => {
        this.loading = false;
      });
  },
  methods: {
    formatDate(dateString) {
      return format(new Date(dateString), 'yyyy-MM-dd HH:mm:ss');
    },
  }
}
</script>

<style scoped>
.v-expansion-panel-header {
  font-size: large;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.panel-content {
  margin-top: 30px;
}
</style>