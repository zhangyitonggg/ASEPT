<template>
  <div>
    <template v-if="loading">
      <v-container fluid class="d-flex align-center justify-center">
        <v-row class="text-center">
          <v-col>
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
          </v-col>
        </v-row>
      </v-container>
      <v-container fluid class="d-flex align-center justify-center">
        <v-row class="text-center">
          <v-col>
            <h3>
              潮平两岸阔，风正一帆悬。
            </h3>
            <h4>
              欢迎回到 ASEPT。
            </h4>
            <span>正在获取公告。</span>
          </v-col>
        </v-row>
      </v-container>
    </template>

    <template v-else>
      <v-row class="pb-10">
        <v-spacer />
        <v-btn large @click="dialog_openannouncement = true" color="primary">
          <v-icon>mdi-plus</v-icon>
          <span>新建公告</span>
        </v-btn>
      </v-row>
      <template>
        <v-expansion-panels inset focusable v-if="news.length > 0">
          <v-expansion-panel v-for="(item, index) in news" :key="index">
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
              <v-btn block @click="initAnnouncementModifyDialog(item)"> 修改公告 </v-btn>
              <v-dialog v-model="dialog_modifyannouncement" width="50%">
                <v-card>
                  <v-card-title>
                    修改公告
                  </v-card-title>
                  <v-card-text>
                    <v-text-field label="公告标题" filled outlined v-model="announcementTitle"></v-text-field>
                    <v-textarea label="公告内容" filled outlined rows="20" v-model="announcementContent"></v-textarea>
                    <v-switch v-model="announcementActive" :label="`${announcementActived}`"></v-switch>
                  </v-card-text>
                  <v-divider></v-divider>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" text @click="modifyAnnouncement(item)" :disabled="loading"
                      :loading="loading"> 修改
                    </v-btn>
                    <v-btn color="error" text @click="dialog_modifyannouncement = false" :disabled="loading"> 取消
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <h2 v-else class="d-flex justify-center align-center">
          好吧，看起来现在还没有公告。
        </h2>
      </template>
    </template>
    <v-dialog v-model="dialog_openannouncement" width="50%">
      <v-card>
        <v-card-title>
          新建公告
        </v-card-title>

        <v-card-text>
          <v-text-field label="公告标题" v-model="announcementTitle"></v-text-field>
          <v-textarea label="公告内容" rows="20" v-model="announcementContent"></v-textarea>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="publishAnnouncement" :disabled="loading" :loading="loading"> 发布 </v-btn>
          <v-btn color="error" text @click="cancelPublishAnnouncement" :disabled="loading"> 取消 </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="js">
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
    VMdPreview,
  },
  data() {
    return {
      dialog_openannouncement: false,
      dialog_modifyannouncement: false,
      news: null,
      loading: true,
      activePanel: 0,
      announcementTitle: "",
      announcementContent: "",
      announcementActive: false,
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
    publishAnnouncement() {
      this.loading = true;
      this.$store.dispatch("publishAnnouncement", {
        title: this.announcementTitle,
        content: this.announcementContent,
      })
        .then(_ => {
          this.$store.commit("setAlert", { type: "success", message: "公告发布成功。" });
          this.loading = true;
          this.$store.dispatch("getNews")
            .then(res => {
              this.news = res.announcements;
            })
            .catch(_ => {
              this.news = [];
              this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
            });
        })
        .catch(_ => {
          this.$store.commit("setAlert", { type: "error", message: "无法发布公告。请检查你的网络设置。" });
        })
        .finally(() => {
          this.dialog_openannouncement = false;
          this.loading = false;
        });
    },
    cancelPublishAnnouncement() {
      this.dialog_openannouncement = false;
    },
    initAnnouncementModifyDialog(item) {
      this.announcementTitle = item.title;
      this.announcementContent = item.content;
      this.announcementActive = item.is_active;
      this.dialog_modifyannouncement = true;
    },
    modifyAnnouncement(item) {
      this.loading = true;
      this.$store.dispatch("modifyAnnouncement", {
        aid: item.aid,
        title: this.announcementTitle,
        content: this.announcementContent,
        is_active: this.announcementActive,
      })
        .then(_ => {
          this.$store.commit("setAlert", { type: "success", message: "公告修改成功。" });
          this.loading = true;
          this.$store.dispatch("getNews")
            .then(res => {
              this.news = res.announcements;
            })
            .catch(_ => {
              this.news = [];
              this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
            });
        })
        .catch(_ => {
          this.$store.commit("setAlert", { type: "error", message: "无法修改公告。请检查你的网络设置。" });
        })
        .finally(() => {
          this.dialog_modifyannouncement = false;
          this.loading = false;
        });
    }
  },
  computed: {
    announcementActived() {
      return this.announcementActive ? "公告状态：有效" : "公告状态：无效";
    }
  },
  watch: {
    dialog_openannouncement(val) {
      this.announcementContent = "";
      this.announcementTitle = "";
    },
    dialog_modifyannouncement(val) {
      if (!val) {
        this.announcementContent = "";
        this.announcementTitle = "";
      }
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