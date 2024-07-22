<template>
  <v-container
    class="spacing-playground pa-16"
    fluid
  >
    <component :is="currentComponent" />

    <v-bottom-navigation
      app
      fixed
      color="primary"
      v-model="activeBtn"
      @change="handleNavigateClick"
    >
      <v-btn value="problems">
        <span>题目</span>
        <v-icon>mdi-lightbulb-question</v-icon>
      </v-btn>
      <v-btn value="problemGroups">
        <span>题单</span>
        <v-icon>mdi-view-list</v-icon>
      </v-btn>
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
import SearchBar from '../components/SearchBar.vue'
import Problem from '../components/exercises/Problem.vue'
import ProblemList from '../components/exercises/ProblemList.vue'
import ProblemManage from '../components/exercises/ProblemManage.vue'
import ListManage from '../components/exercises/ListManage.vue'
export default {
  name: 'HomeView',
  components: {
    Problem,
    ProblemList,
    ListManage,
    ProblemManage,
    SearchBar
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
        case 'problems':
          return 'Problem';
        case 'problemGroups':
          return 'ProblemList';
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
          case 'problemGroups':
            return '题单';
          case 'manageProblemGroups':
            return '管理题单';
          default:
            return '题目';
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