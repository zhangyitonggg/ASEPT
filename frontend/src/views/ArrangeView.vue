<template>
  <div>
    <v-container fluid class="d-flex justify-center align-center" v-if="loading">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-container>
    <v-container class="spacing-playground pa-16" fluid v-else>
      <v-layout>
        <v-flex xs1>
          <v-btn color="success" @click="getAgain">换一批</v-btn>
        </v-flex>

        <v-spacer />
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索推荐题目' />
        </v-flex>
      </v-layout>

      <v-col>
        <v-list three-line>
          <template v-for="(item, index) in filteredItems">
            <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>
            <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>
            <v-list-item v-else-if="item.title" :key="item.pid">
              <v-list-item-avatar>
                <v-icon> mdi-help-circle-outline</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>
                  <h4>
                    {{ item.title }}
                  </h4>
                </v-list-item-title>
                <v-list-item-subtitle>
                  Tag: {{ item.tag }}
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn color="primary" @click="solveProblem(item)"> 再刷一遍 </v-btn>
              </v-list-item-action>

            </v-list-item>
          </template>
        </v-list>
      </v-col>
    </v-container>
  </div>
</template>

<script>
import searchbar from '../components/SearchBar.vue'
export default {
  name: 'ArrangeView',
  components: {
    searchbar
  },
  data() {
    return {
      search: '',
      loading: true,
      keys: [
        'Name',
        'Tag',
      ],
      items: [

      ],
    }
  },
  computed: {
    filteredItems() {
      const filtered = this.items.filter(item =>
      ((item.title && item.title.toLowerCase().includes(this.search.toLowerCase())) ||
        (item.tag && item.tag.toLowerCase().includes(this.search.toLowerCase())) ||
        (item.content && item.content.toLowerCase().includes(this.search.toLowerCase())))
      );
      return filtered;
    },
  },
  mounted() {
    this.$store.commit('setAppTitle', '推荐题目');
    this.getProblemsRecommended();
  },
  methods: {
    getAgain() {
      this.getProblemsRecommended();
    },
    getProblemsRecommended() {
      this.$store
        .dispatch('getProblemsRecommended')
        .then(res => {
          this.items.splice(0, this.items.length, { header: '推荐题目' }, ...res.problems); // 清空当前数组并插入新数据
          console.log("推荐题目：", this.items);
        })
        .catch(error => {
          this.$store.commit("setAlert", {
            type: "error",
            message: error,
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    solveProblem(item) {
      this.$router.push({ path: 'solve/' + item.pid, append: true });
    },
  },
  watch: {

  }
}
</script>

<style scoped>
.scrollable-container {
  position: relative;
  top: -10%;
  height: 100%;
  overflow: auto;
}

.header-title {
  font-size: 18px;
  font-weight: 500;
  color: #ffffff;
  margin-right: 30%;
}

.pagination-info {
  font-size: 16px;
  font-weight: bold;
  margin-left: 2%;
  /* Adjust as needed to move it slightly to the right */
}

.item-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.description-text {
  display: block;
  white-space: normal;
  /* Allow text to wrap onto multiple lines */
}

.apply-button {
  font-size: 14px;
  position: absolute;
  color: white;
  font-weight: 900;
  top: 15px;
  right: 20px;
}
</style>
