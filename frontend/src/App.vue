<template>
    <v-app id="inspire">
      <v-app-bar
        app
        v-if="$store.state._show_platform_frame_"
      >
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        <v-toolbar-title>{{ $store.state._app_title_ }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <clock class="pr-3"/>
        <div class="pr-3">{{ getCurrentTimeGreetings() }}，{{ $store.getters.username }}</div>
          <v-menu
            bottom
            min-width="130px"
            rounded
            offset-y
          > <template v-slot:activator="{ on }">
              <v-btn
                icon
                v-on="on"
              >
                <v-avatar
                  size="36"
                >
                <img src="https://cravatar.cn/avatar/5ed20f2960c5e87468dee55bfd3ec4ab?d=mp">
                </v-avatar>
              </v-btn>
            </template>
            <v-card>
              <v-list-item-content class="justify-center">
                <div class="mx-auto text-center">
                  <v-btn
                    depressed
                    rounded
                    text
                    @click="navigateTo('/me')"
                  >
                    个人中心
                  </v-btn>
                  <v-divider class="my-3"></v-divider>
                  <v-btn
                    rounded
                    text
                    color="error"
                    @click="logout"
                  >
                    注销
                  </v-btn>
                </div>
              </v-list-item-content>
            </v-card>
          </v-menu>
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
        v-show="$store.state._alert_.show"
        :type="$store.state._alert_.type"
        transition="scroll-y-transition"
      >{{ $store.state._alert_.message }}
      </v-alert>
    </v-app>
  </template>

<script lang="ts">
import Vue from 'vue';
import clock from './components/TimeClock.vue';

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
        ['mdi-account', '个人中心', '/me'],
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
    },
    getCurrentTimeGreetings() {
      const h = new Date().getHours()
      if (h < 2) return '夜深了'
      if (h < 6) return '别卷了'
      if (h < 12) return '上午好'
      if (h < 13) return '中午好'
      if (h < 18) return '下午好'
      if (h < 23) return '晚上好'
      return '夜深了'
    },
    logout() {
      this.$store.commit("clearPersonalInfo");
      this.$router.push({ name: 'login' });
    }
  },
  components: {
    clock,
  },
  created() {
    if (localStorage.getItem('__token__') && localStorage.getItem('__user_name__')) {
      this.$store.commit('setAlert', {
        type: "success",
        message: "欢迎回来，" + localStorage.getItem('__user_name__') + "。",
      });
    }
  },
  beforeCreate() {
    if (localStorage.getItem('__dark_theme__')) {
      this.$vuetify.theme.dark = localStorage.getItem('__dark_theme__') === 'true';
    }
  }
});

export default App;
</script>

<style lang="scss">
@import './assets/styles/main.scss';

.v-alert {
  z-index: 1001;
  position: fixed;
  bottom: 0;
  width: 100%;
  left: 0;
}

.slide-y-enter-active, .slide-y-leave-active {
  transition: all 0.5s ease;
}
.slide-y-enter, .slide-y-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>