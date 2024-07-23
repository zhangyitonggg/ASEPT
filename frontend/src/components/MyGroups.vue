<template>
  <div>
    <v-container fluid>
        <v-layout>
          <v-spacer/>
          <searchbar v-model="search" searchBtnText='搜索团队'/>
        </v-layout>
        <v-col>
          <v-list three-line>
            <template v-for="(item, index) in currentPageItems">
              <v-divider inset></v-divider>
              <v-subheader
                v-if="item.header"
                :key="item.header"
                v-text="item.header"
              ></v-subheader>
              <v-list-item
                v-else-if="item.group_name"
                :key="item.group_name"
              >
                <v-list-item-avatar>
                  <v-icon> {{ item.need_password ? "mdi-link-lock" : "mdi-link"}}</v-icon>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>
                    <h4>
                      {{ item.group_name }}
                    </h4>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Founder: 
                    <strong>
                      {{ item.founder }}
                    </strong>
                    <br>
                      {{ item.description }}
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn
                    color="warning"
                    @click="leave(item)"
                  > 离开 </v-btn>
                </v-list-item-action>
              </v-list-item>
            </template>
            <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
          </v-list>
        </v-col>
    </v-container>
    <v-row justify="center">
      <v-dialog
        v-model="dialog"
        max-width="290"
      >
        <v-card>
          <v-card-title class="text-h7">
            确定要离开 {{curItem.group_name}} 吗？
          </v-card-title>

           <v-card-actions>
            <v-spacer></v-spacer>
  
            <v-btn
              color="green darken-1"
              text
              @click="handleAboutClick(false)"
            >
              取消
            </v-btn>
  
            <v-btn
              color="red darken-1"
              text
              @click="handleAboutClick(true)"
            >
              确定
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
import searchbar from './SearchBar.vue'

export default {
  data () {
    return {
      dialog: false,
      curItem: {},
      search: '',
      filter: {},
      page: 1,
      currentPage: 1,
      itemsPerPage: 13,
      items: [],
    }
  },
  computed: {
    numberOfPages () {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage)
    },
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.group_name && item.group_name.toLowerCase().includes(this.search.toLowerCase())
      );
      // console.log('Filtered Items:', filtered); // 调试输出
      return filtered;
    },
    currentPageItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredItems.slice(startIndex, endIndex);
    },
  },
  mounted() {
    this.getJoinedGroups();
  },
  methods: {
    getJoinedGroups() {
      this.$store
        .dispatch("showJoinedGroups")
        .then((res) => {
          this.items.splice(0, this.items.length, { header: '所有已加入的团队' }, ...res.groups); // 清空当前数组并插入新数据
          console.log(this.items);
        })
        .catch((e) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: e,
          });
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
    leave(item) {
      this.curItem = item;
      this.dialog = true;
    },
    handleAboutClick(flag) {
      this.dialog = false;
      if (flag) {
        this.$store
        .dispatch("leaveGroup",{gid: this.curItem.gid})
        .then((res) => {
          if (flag) {
            alert(`你选择了离开 ${this.curItem.group_name}`);
            const index = this.items.findIndex(item => item.gid === this.curItem.gid);
            if (index !== -1) {
              this.items.splice(index, 1);
            }
          }
        })
        .catch((e) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: e,
          });
        });
      }
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
