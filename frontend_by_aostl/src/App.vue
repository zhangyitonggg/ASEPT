<template>
    <v-app id="inspire">
      <v-app-bar
        app
        v-if="$store.state._show_platform_frame_"
      >
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        <v-app-bar-title>Application</v-app-bar-title>
        <v-spacer></v-spacer>
        <div>别卷了，{{ $store.state._user_name_ }}</div>
      </v-app-bar>
      <v-navigation-drawer
        v-model="drawer"
        fixed
        temporary>
        <div class="d-flex flex-column" style="height: 100%;">
          <v-list class="flex-grow-1">
            <v-list-item
              v-for="[icon, text, route] in links"
              :key="icon"
              link
              @click="navigateTo(route)">
              <v-list-item-icon>
                <v-icon>{{ icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ text }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-spacer></v-spacer>
          <v-list>
            <v-list-item link @click="handleAboutClick" class="about-btn">
              <v-list-item-icon>
                <v-icon>mdi-progress-question</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>关于</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </div>
      </v-navigation-drawer>
      <v-main>
        <router-view />
      </v-main>
      <v-alert
        elevation="11"
        :type="this.$store.state._alert_.type"
        v-show="this.$store.state._alert_.show"
        transition="scroll-y-transition"
      >{{ this.$store.state._alert_.message }}</v-alert>
    </v-app>
  </template>

<script lang="ts">
import Vue from 'vue';
import store from '@/store'

const App = Vue.extend({
  name: 'App',

  data() {
    return {
      drawer: null,
      links: [
        ['mdi-home', '首页', '/'],
        ['mdi-book-open-variant-outline', '题库', '/exercises'],
        ['mdi-account-group', '团队', '/groups'],
        ['mdi-head-lightbulb-outline', '精心安排', '/arrange'],
        ['mdi-account', '个人中心', '/mine'],
      ],
    };
  },

  computed: {
  },

  methods: {
    navigateTo(route) {
      this.$router.push(route).catch(err => {
      if (err.name !== 'NavigationDuplicated') {
        throw err;
      }
    });
    },
    handleAboutClick() { // 处理关于按钮点击事件
      this.navigateTo('/about');
    }
  },

  components: {
  },

  created() {
    if (localStorage.getItem('__token__') && localStorage.getItem('__user_name__')) {
      this.$store.commit('setAlert', {
        type: "success",
        message: "欢迎回来，" + localStorage.getItem('__user_name__') + "。",
      });
    }
  }
});

export default App;
</script>

<style lang="scss">
@import './assets/styles/main.scss';

.v-alert {
  z-index: 1001;
}

.slide-y-enter-active, .slide-y-leave-active {
  transition: all 0.5s ease;
}
.slide-y-enter, .slide-y-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>