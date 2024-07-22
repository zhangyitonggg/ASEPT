<template>
  <v-container
    class="spacing-playground pa-16"
    fluid
  > <component :is="this.activeBtn" />
    <v-bottom-navigation
      app
      fixed
      color="primary"
      v-model="activeBtn"
      @change="handleNavigateClick"
    >
      <v-btn value="myinfo">
        <span>个人信息</span>
        <v-icon>mdi-account-settings</v-icon>
      </v-btn>
      <v-btn value="fontSetting">
        <span>页面设置</span>
        <v-icon>mdi-cog</v-icon>
      </v-btn>
      <v-btn value="feedback">
        <span>反馈</span>
        <v-icon>mdi-invoice</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-container>
</template>

<script>
import myinfo from '../components/MyInfo.vue'
import feedback from '../components/Feedback.vue'

export default {
  name: 'HomeView',
  components: {
    myinfo,
    feedback,
  },
  data() {
    return {
      activeBtn: 'myinfo',
      loading: true,
    }
  },
  computed: {
  },
  methods: {
    handleNavigateClick(newValue) {
      this.$store.commit('setAppTitle', (() => {
        switch (newValue) {
          case 'fontSetting':
            return '页面设置';
          case 'feedback':
            return '反馈';
          default:
            return '个人信息';
        }
      })());
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