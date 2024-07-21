<template>
  <v-container>
    <component :is="currentComponent"></component>
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
        <v-icon>mdi-account-plus</v-icon>
      </v-btn>
      <v-btn value="manage">
        <span>管理团队</span>
        <v-icon>mdi-account-supervisor-circle</v-icon>
      </v-btn>
      <v-btn value="create">
        <span>创建团队</span>
        <v-icon>mdi-account-multiple-plus-outline</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-container>
</template>

<script>
import EnterGroup from '@/components/EnterGroup.vue';
import MyGroups from '@/components/MyGroups.vue';
import GroupCreated from '@/components/GroupCreated.vue';
import CreateGroup from '@/components/CreateGroup.vue';

export default {
  name: 'GroupView',
  components: {
    EnterGroup,
    MyGroups,
    GroupCreated,
    CreateGroup
  },
  data() {
    return {
      activeBtn: 'mygroups',
    }
  },
  methods: {
    handleNavigateClick(newValue) {
      this.$store.commit("setAppTitle", newValue === 'mygroups' ? '我的团队' : newValue === 'join' ? '加入团队' : newValue === 'manage' ? '管理团队' : '创建团队');
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
        case 'create':
          return 'CreateGroup';
        default:
          return 'MyGroups';
      }
    }
  },
}
</script>