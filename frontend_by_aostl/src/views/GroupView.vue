<template>
  <v-container>
    <v-main>
      <component :is="currentComponent"></component>
    </v-main>
    <v-footer height="0">
      <v-bottom-navigation
        app
        fixed
        color="primary"
        v-model="activeBtn"
        @change="handleNavigateClick"
      >
        <v-btn value="mygroups">
          <span>我的团队</span>
          <v-icon>mdi-account-group-outline</v-icon>
        </v-btn>
        <v-btn value="join">
          <span>加入团队</span>
          <v-icon>mdi-account-multiple-plus</v-icon>
        </v-btn>
        <v-btn value="manage">
          <span>管理团队</span>
          <v-icon>mdi-account-supervisor-circle</v-icon>
        </v-btn>
      </v-bottom-navigation>
    </v-footer>
  </v-container>
</template>

<script>
import EnterGroup from '@/components/EnterGroup.vue';
import MyGroups from '@/components/MyGroups.vue';
import GroupCreated from '@/components/GroupCreated.vue';

export default {
  name: 'GroupView',
  components: {
    EnterGroup,
    MyGroups,
    GroupCreated
  },
  data() {
    return {
      activeBtn: 'mygroups',
    }
  },
  methods: {
    handleNavigateClick(newValue) {
      this.$store.commit("setAppTitle", newValue === 'mygroups' ? '我的团队' : newValue === 'join' ? '加入团队' : '管理团队');
    },
  },
  watch: {
  },
  mounted() {
    this.$store.commit("setAppTitle", '我的团队');
  },
  computed: {
    currentComponent() {
      switch (this.activeBtn) {
        case 'join':
          return 'EnterGroup';
        case 'manage':
          return 'GroupCreated';
        default:
          return 'MyGroups';
      }
    }
  },
}
</script>

<style scoped>
</style>
