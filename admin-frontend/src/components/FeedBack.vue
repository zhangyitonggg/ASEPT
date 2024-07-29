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
              <h3>当年明月在，不见彩云归。</h3>
              <span>正在获取用户反馈。</span>
            </v-col>
          </v-row>
        </v-container>
      </template>
  
      <template v-else>
        <v-expansion-panels inset focusable v-if="feedbacks.length > 0">
          <v-expansion-panel v-for="(feedback, index) in feedbacks" :key="index">
            <v-expansion-panel-header :disable-icon-rotate="!feedback.is_active">
              <div style="display: flex; justify-content: space-between; width: 100%;">
                <div>{{ feedback.name }}的反馈</div>
                <div style="color: grey; text-align: right; margin-right: 16px;">
                  <span>{{ formatDate(feedback.update_time) }}</span>
                </div>
              </div>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <div class="panel-content">
                <div><strong>Username:</strong> {{ feedback.username }}</div>
                <div><strong>Email:</strong> {{ feedback.email }}</div>
                <div><strong>Advice:</strong> {{ feedback.advice }}</div>
                <div><strong>Complaint:</strong> {{ feedback.complaint }}</div>
              </div>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <h2 v-else class="d-flex justify-center align-center">
          好吧，看起来现在还没有反馈。
        </h2>
      </template>
    </div>
  </template>
  
  <script>
  import { format } from 'date-fns';
  
  export default {
    data() {
      return {
        feedbacks: [],
        loading: true,
      }
    },
    mounted() {
      this.$store.commit("setAppTitle", "用户反馈");
      this.$store.dispatch("getFeedbacks")
        .then(res => {
          this.feedbacks = res.feedbacks;
        })
        .catch(_ => {
          this.feedbacks = [];
          this.$store.commit("setAlert", { type: "error", message: "无法获取反馈。请检查你的网络设置。" })
        })
        .finally(() => {
          this.loading = false;
        });
    },
    methods: {
      formatDate(dateString) {
        return format(new Date(dateString), 'yyyy-MM-dd HH:mm:ss');
      }
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
  