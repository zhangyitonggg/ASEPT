<template>
  <div>
    <v-expansion-panels inset>
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
          <div>
            <p>{{ item.content }}</p>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { vuetify } from 'vuetify';
import { format } from 'date-fns';

export default {
  name: "NewsList",
  data() {
    return {
      news: null
    }
  },
  mounted() {
    this.$store.commit("setAppTitle", "公告");
    this.$store.dispatch("getNews")
      .then(res => {
        this.news = res.announcements;
      })
      .catch(errpr => {
        console.log(errpr);
        this.$store.commit("setAlert", {type: "error", message: "无法获取公告。请检查你的网络设置。"})
      })
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
</style>