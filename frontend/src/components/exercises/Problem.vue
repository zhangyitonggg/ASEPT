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
            <h3>
              苟日新，日日新，又日新。
            </h3>
            <span>正在获取题目。</span>
          </v-col>
        </v-row>
      </v-container>
    </template>
    <v-container fluid v-else>
      <v-layout>
        <!-- 查找题目按钮 -->
        <v-btn color="primary" @click="openSearchDialog">查找题目</v-btn>
        <v-spacer />
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索题目' />
        </v-flex>
      </v-layout>
      <v-col>
        <v-list three-line>
          <v-subheader>题目列表</v-subheader>
          <template v-for="(item, index) in currentPageItems">
            <v-divider v-if="item.divider" :inset="item.inset"></v-divider>
            <v-list-item v-else :key="item.pid">
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
                  Tag: {{ item.tagsString }}
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn color="primary" @click="solveProblem(item)"> 去做题 </v-btn>
              </v-list-item-action>
            </v-list-item>
          </template>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-list>
      </v-col>

      <!-- 查找题目弹窗 -->
      <v-dialog v-model="showSearchDialog" max-width="800px">
        <v-card>
          <v-card-title>
            查找题目
            <v-spacer></v-spacer>
            <v-btn icon @click="showSearchDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="searchProblems">
              <v-select v-model="searchTag" :items="tags" item-text="tag_name" item-value="tid" label="选择标签" outlined
                clearable></v-select>
              <v-text-field v-model="searchKeyword" label="关键词" outlined></v-text-field>
              <v-btn color="primary" type="submit">搜索</v-btn>
            </v-form>
            <v-list three-line>
              <template v-for="problem in searchResults">
                <v-list-item>
                  <v-list-item-avatar>
                    <v-icon>mdi-help-circle-outline</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>{{ problem.title }}</v-list-item-title>
                    <v-list-item-subtitle>{{ problem.content }}</v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn color="primary" @click="solveProbleminTag(problem)">去做题</v-btn>
                  </v-list-item-action>
                </v-list-item>
              </template>
            </v-list>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script>
import searchbar from '../SearchBar.vue';

export default {
  data() {
    return {
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      loading: true,
      itemsPerPage: 13,
      currentPage: 1,
      sortBy: 'name',
      keys: ['Name', 'Tag'],
      items: [],
      showSearchDialog: false,
      searchTag: '',
      searchResults: [],
      searchKeyword: '',
      tags: [], // 用于存储获取到的标签
    };
  },
  created() {
    this.fetchProblems();
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage);
    },
    filteredKeys() {
      return this.keys.filter(key => key !== 'Name');
    },
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.title && item.title.toLowerCase().includes(this.search.toLowerCase())
      );
      return filtered;
    },
    currentPageItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredItems.slice(startIndex, endIndex).map(item => {
        return {
          ...item,
          tagsString: item.tags.join(' '),
        };
      });
    },
  },
  watch: {
    search() {
      this.currentPage = 1;
    },
    numberOfPages(newVal) {
      if (this.currentPage > newVal) {
        this.currentPage = newVal;
      }
    }
  },
  methods: {
    fetchProblems() {
      this.$store
        .dispatch('getAllProblems')
        .then(res => {
          this.items = [{ header: '我创建的题目' }, ...res.problems];
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    updateItemsPerPage(number) {
      this.itemsPerPage = number;
    },
    solveProblem(item) {
      this.$store.commit('setCurrentProblemGroup', { problems: this.items.slice(1) });
      this.$router.push({ path: 'solve/' + item.pid, append: true });
    },
    solveProbleminTag(item) {
      this.$store.commit('setCurrentProblemGroup', { problems: this.searchResults });
      this.$router.push({ path: 'solve/' + item.pid, append: true });
    },
    searchProblems() {
      let mytag = this.searchTag;
      let mykeyword = this.searchKeyword || '';
      this.$store
        .dispatch('searchProblemByTag', { tag: mytag, keyword: mykeyword })
        .then(res => {
          this.searchResults = res.problems;
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    openSearchDialog() {
      this.showSearchDialog = true;
      this.fetchTags();
    },
    fetchTags() {
      this.$store
        .dispatch('getProblemTags')
        .then(res => {
          this.tags = res.tags;
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    selectTag(tag) {
      this.searchTag = tag;
    },
  },
  components: {
    searchbar,
  },
};
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

.tags-container {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10px;

}

.ma-2 {
  margin: 5px;
}
</style>
