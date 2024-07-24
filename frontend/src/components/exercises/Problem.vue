<template>
  <v-container fluid>
      <v-layout>
        <v-spacer/>
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索题目'/>
        </v-flex>
      </v-layout>
      <v-col>
        <v-list three-line>
          <template v-for="(item, index) in currentPageItems">
            <!-- <v-subheader
              v-if="item.header"
              :key="item.header"
              v-text="item.header"
            ></v-subheader> -->
            <v-divider
              v-if="item.divider"
              :key="index"
              :inset="item.inset"
            ></v-divider>
            <v-list-item
              v-else-if="item.title"
              :key="item.pid"
            >
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
                <v-btn
                  color="primary"
                  @click="solveProblem(item)"
                > 去做题 </v-btn>
              </v-list-item-action>

            </v-list-item>
          </template>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-list>
      </v-col>
  </v-container>
</template>

<script>
import searchbar from '../SearchBar.vue'

export default {
  data () {
    return {
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 13,
      currentPage: 1,
      sortBy: 'name',
      keys: [
        'Name',
        'Tag',
      ],
      items: [
        { header: '题目列表' },
        {
          name: 'Problem1',
          tag: 'Descrlines.',
          gid: 'xxx1',
          locked: true,
          content: '66666666',
        },
        { divider: true, inset: true },
        {
          name: 'Group2',
          //founder: 'User2',
          tag: 'Descrlines.',
          gid: 'xxx2',
          locked: true,
        },
        { divider: true, inset: true },
        {
          name: 'Group3',
          founder: 'User3',
          description: 'Descrlines.',
          gid: 'xxx3',
          locked: false,
        },
        { divider: true, inset: true },
        
      ],
    }
  },
  created() {
    this.fetchProblems();
  },
  computed: {
    numberOfPages () {
      return Math.ceil(this.items.length / this.itemsPerPage)
    },
    filteredKeys () {
      return this.keys.filter(key => key !== 'Name')
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
      return this.filteredItems.slice(startIndex, endIndex);
    },
  },
  methods: {
     fetchProblems() {
        this.$store
        .dispatch('getMyProblem')
        .then(res => {
          // this.items = response.problems.map(problem => {
          //   return {
          //     pid: problem.pid,
          //     title: problem.title,
          //     content: problem.content,
          //     type: problem.type === 0 ? 'SINGLE_CHOICE' : 'MULTIPLE_CHOICE',
          //     author: problem.author,
          //     upload_time: problem.upload_time,
          //     choices: problem.choices,
          //     answers: problem.answers,
          //     s_public: problem.is_public === 1,
          //   }
          // });
          this.items.splice(0, this.items.length, { header: '我创建的题目' }, ...res.problems); // 清空当前数组并插入新数据
          console.log("我创建的：",this.items);
        })
        .catch(error => {
             this.$store.commit("setAlert", {
             type: "error",
            message: error,
          });
          }).finally(() => {
          this.loading = false;
        });
    },
    nextPage () {
      if (this.page + 1 <= this.numberOfPages) this.page += 1
    },
    formerPage () {
      if (this.page - 1 >= 1) this.page -= 1
    },
    updateItemsPerPage (number) {
      this.itemsPerPage = number
    },
    solveProblem(item){
      console.log('pid:',item.pid );
      this.$router.push({path:'solve/' + item.pid, append:true});
    },
  },
  components: {
    searchbar
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
  font-weight:900;
  top: 15px;
  right: 20px;
}
</style>
