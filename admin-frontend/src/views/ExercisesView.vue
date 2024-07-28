<template>
  <v-container class="spacing-playground pa-16" fluid>
    <component :is="currentComponent" />

    <v-bottom-navigation app fixed color="primary" v-model="activeBtn" @change="handleNavigateClick">
      <v-btn value="manageProblemGroups">
        <span>管理题单</span>
        <v-icon>mdi-window-shutter-cog</v-icon>
      </v-btn>
      <v-btn value="manageProblems">
        <span>管理题目</span>
        <v-icon>mdi-file-cog</v-icon>
      </v-btn>
    </v-bottom-navigation>
  </v-container>
</template>

<script>
import ProblemManage from '../components/exercises/ProblemManage.vue'
import ListManage from '../components/exercises/ListManage.vue'
export default {
  name: 'HomeView',
  components: {
    ListManage,
    ProblemManage,
  },
  data() {
    return {
      activeBtn: 'problems',
      loading: true,
      exercises: [
        { id: 1, name: 'Pushups' },
        { id: 2, name: 'Situps' },
        { id: 3, name: 'Squats' },
      ],
    }
  },
  computed: {
    currentComponent() {
      switch (this.activeBtn) {
        case 'manageProblemGroups':
          return 'ListManage';
        default:
          return 'ProblemManage';
      }
    }
  },
  methods: {
    handleNavigateClick(newValue) {
      this.$store.commit('setAppTitle', (() => {
        switch (newValue) {
          case 'manageProblems':
            return '管理题目';
          default:
            return '管理题单';
        }
      })());
    },
  },
  watch: {
  },
  mounted() {
    this.$store.commit('setAppTitle', '题目');
  },
}
</script>

<style scoped>
.v-bottom-navigation {
  bottom: 0;
}
</style>