<template>
  <v-container fluid>
    <v-layout>
      <!-- 创建题单按钮 -->
      <v-flex xs1>
        <v-btn color="primary" @click="showCreateDialog = true">创建题单</v-btn>
      </v-flex>
      <v-spacer/>
      <v-flex xs24>
        <searchbar v-model="search" searchBtnText='搜索题单'/>
      </v-flex>
    </v-layout>
    
    <v-col>
      <v-list three-line>
        <template v-for="(item, index) in currentPageItems">
          <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>
          <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>
          <v-list-item v-else-if="item.pgid" :key="item.pgid">
            <v-list-item-avatar>
              <v-icon>{{ item.locked ? 'mdi-link-lock' : 'mdi-link' }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                <h4>{{ item.name }}</h4>
              </v-list-item-title>
              <v-list-item-subtitle>
                Tag: {{ item.tag }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn color="primary" @click="shareList(item)"> 分享题单 </v-btn>
            </v-list-item-action>
          </v-list-item>
        </template>
        <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
      </v-list>
    </v-col>

    <!-- 创建题单弹窗 -->
    <v-dialog v-model="showCreateDialog" max-width="500px">
      <v-card>
        <v-card-title>
          创建新题单
          <v-spacer></v-spacer>
          <v-btn icon @click="showCreateDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="createList">
            <v-text-field v-model="newListName" label="题单名称" required></v-text-field>
            <v-textarea v-model="newListDescription" label="描述"></v-textarea>
            <v-card-actions>
              <v-btn color="primary" type="submit">创建</v-btn>
              <v-btn text @click="showCreateDialog = false">取消</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import searchbar from '../SearchBar.vue';
export default {
  data() {
    return {
      showCreateDialog: false,
      newListName: '',
      newListDescription: '',
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 13,
      sortBy: 'name',
      keys: ['Name', 'Tag'],
      items: [],
      currentPage: 1,
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
      return this.keys.filter(key => key !== 'Name');
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
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
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
    shareList(item) {
      alert('你没有好u呢~');
    },
    createList() {
      if (this.newListName) {
        const newList = {
          name: this.newListName,
          description: this.newListDescription,
          locked: false,
        };

        this.$store
        .dispatch('createProblemList',newList)
        .then(response =>{
           this.items.push(newList);
           this.showCreateDialog = false;
          this.newListName = '';
          this.newListDescription = '';
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
      } else {
        alert('请填写题单名称！');
      }
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
</style>
