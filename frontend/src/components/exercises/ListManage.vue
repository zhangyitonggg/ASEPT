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
              万事俱备，只欠东风。
            </h3>
            <span>正在获取你管理的题单。</span>
          </v-col>
        </v-row>
      </v-container>
    </template>
    <v-container fluid v-else>
      <v-layout>
        <!-- 创建题单按钮 -->
        <v-flex xs1>
          <v-btn color="primary" @click="showCreateDialog = true">创建题单</v-btn>
        </v-flex>
        <v-spacer />
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索题单' />
        </v-flex>
      </v-layout>

      <v-col>
        <v-list three-line>
          <template v-for="(item, index) in currentPageItems">
            <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>
            <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>
            <v-list-item v-else-if="item.pgid" :key="item.pgid">
              <v-list-item-avatar>
                <v-icon>mdi-invoice-list-outline</v-icon>
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
                <v-btn color="primary" @click="openShareDialog(item)"> 分享题单 </v-btn>
              </v-list-item-action>
            </v-list-item>
            <v-divider v-if="index < currentPageItems.length - 1"></v-divider>
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

      <!-- 分享题单弹窗 -->
      <v-dialog v-model="showShareDialog" max-width="500px">
        <v-card>
          <v-card-title>
            分享题单
            <v-spacer></v-spacer>
            <v-btn icon @click="showShareDialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="shareList">
              <v-select v-model="selectedGroup" :items="groups" item-text="group_name" item-value="gid" label="选择群组"
                required></v-select>
              <v-card-actions>
                <v-btn color="primary" type="submit">分享</v-btn>
                <v-btn text @click="showShareDialog = false">取消</v-btn>
              </v-card-actions>
            </v-form>
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
      showCreateDialog: false,
      showShareDialog: false,
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
      groups: [],
      loading: true,
      selectedGroup: null,
      selectedItem: null, // 用于保存当前选中的题单
    };
  },
  components: {
    searchbar,
  },
  created() {
    this.fetchItems();
    this.fetchGroups();
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
    fetchItems() {
      this.$store
        .dispatch('getMyProblemGroup')
        .then((res) => {
          this.items = res.problem_groups;
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
    fetchGroups() {
      this.$store
        .dispatch('showJoinedGroups')
        .then((res) => {
          this.groups = res.groups;
        })
        .catch((error) => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    openShareDialog(item) {
      this.selectedItem = item;
      this.showShareDialog = true;
    },
    shareList() {
      if (this.selectedGroup && this.selectedItem) {
        const data = {
          pgid: this.selectedItem.pgid,
          gid: this.selectedGroup,
        };

        this.$store
          .dispatch('shareProblemList', data)
          .then(() => {
            this.showShareDialog = false;
            this.$store.commit('setAlert', {
              type: 'success',
              message: '题单分享成功',
            });
          })
          .catch((error) => {
            this.$store.commit('setAlert', {
              type: 'error',
              message: error,
            });
          });
      } else {
        this.$store.commit('setAlert', {
          type: 'error',
          message: '请选择群组',
        });
      }
    },
    createList() {
      if (this.newListName) {
        const newList = {
          name: this.newListName,
          description: this.newListDescription,
          locked: false,
        };

        this.$store
          .dispatch('createProblemList', newList)
          .then(() => {
            this.items.push(newList);
            this.showCreateDialog = false;
            this.newListName = '';
            this.newListDescription = '';
          })
          .catch((error) => {
            this.$store.commit('setAlert', {
              type: 'error',
              message: error,
            });
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
