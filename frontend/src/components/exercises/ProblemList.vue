

<template>
  <div>
    <v-container fluid class="d-flex justify-center align-center" v-if="loading">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
    </v-container>
    <v-container fluid v-else>
      <v-layout>
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索题单'/>
        </v-flex>
      </v-layout>
      <v-col>
        <v-list three-line>
          <template v-for="(item, index) in currentPageItems">
            <v-subheader
              v-if="item.header"
              :key="item.header"
              v-text="item.header"
            ></v-subheader>
            <v-divider
              v-else-if="item.divider"
              :key="index"
              :inset="item.inset"
            ></v-divider>
            <v-list-item v-else-if="item.pgid" :key="item.pgid">
              <v-list-item-avatar>
                <v-icon> mdi-invoice-list-outline</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title>
                  <h4>{{ item.name }}</h4>
                </v-list-item-title>
                <v-list-item-subtitle>
                  Description: {{ item.description }}
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn color="primary" @click="openDialog(item)">查看题单</v-btn>
              </v-list-item-action>
            </v-list-item>
             <v-divider v-if="index < currentPageItems.length - 1"></v-divider>
          </template>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-list>
      </v-col>
  
    
      <v-dialog v-model="dialog" max-width="800px">
        <v-card>
          <v-card-title class="titlebig">
            题单详情
            <v-spacer></v-spacer>
            <v-btn icon @click="dialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title><br/>
          <v-card-subtitle class="big">
            题单名称: {{ currentItem.name }}
          </v-card-subtitle>
          <v-card-subtitle class="big">
            题目数量: {{ currentItem.problems.length }}
          </v-card-subtitle>
          <v-card-text>
            <v-list three-line>
              <v-list-item-group v-for="(problem, index) in currentItem.problems" :key="index">
                <v-list-item>
                  <v-list-item-avatar>
                    <v-icon>mdi-lightbulb-on-outline</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>
                      题目 {{ index + 1 }}: {{ problem.title }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      Tag: {{ problem.tag }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                      {{ problem.description }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn color="primary" @click="startProblem(problem)">去做题</v-btn>
                  </v-list-item-action>
                </v-list-item>
                <v-divider v-if="index < currentItem.problems.length - 1"></v-divider>
              </v-list-item-group>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="dialog = false">关闭</v-btn>
          </v-card-actions>
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
      dialog: false,
      currentItem: { name: '', tag: '', problems: [] }, // 更新为包含题目数组
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      loading: true,
      page: 1,
      itemsPerPage: 13,
      currentPage: 1,
      sortBy: 'name',
      keys: ['Name', 'Tag'],
      items: [],
    };
  },
  components: {
    searchbar,
  },
  created() {
    this.fetchItems();
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
    filteredKeys() {
      return this.keys.filter((key) => key !== 'Name');
    },
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.name && item.name.toLowerCase().includes(this.search.toLowerCase())
      );
      return filtered;
    },
    currentPageItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredItems.slice(startIndex, endIndex);
    },
  },
  methods: {
    fetchItems() {
      this.$store
        .dispatch('getProblemGroup')
        .then((res) => {
          this.items = res.problem_groups;
          console.log('groups: ', this.items);
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        })
        .finally(() => {  
          this.loading = false;
        });
    },
    nextPage() {
      if (this.page + 1 <= this.numberOfPages) this.page += 1;
    },
    formerPage() {
      if (this.page - 1 >= 1) this.page -= 1;
    },
    updateItemsPerPage(number) {
      this.itemsPerPage = number;
    },
    openDialog(item) {
      this.$store
        .dispatch('getProblemsInList', { pgid: item.pgid })
        .then((res) => {
          this.currentItem = {
            name: item.name,
            tag: item.tag,
            problems: res.problems,
          };
          this.dialog = true;
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    startProblem(problem) {
      this.$router.push({ path: 'solve/' + problem.pid, append: true });
    },
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
  margin-left: 2%; /* Adjust as needed to move it slightly to the right */
}

.item-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
}

.description-text {
  display: block;
  white-space: normal; /* Allow text to wrap onto multiple lines */
}

.apply-button {
  font-size: 14px;
  position: absolute;
  color: white;
  font-weight: 900;
  top: 15px;
  right: 20px;
}

.big {
  font-size: 18px;
}

.titlebig {
  font-size: 35px;
}
</style>

