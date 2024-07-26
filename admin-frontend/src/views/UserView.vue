<template>
    <v-container>
      <div>
        <v-container fluid class="d-flex justify-center align-center" v-if="loading">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
          ></v-progress-circular>
        </v-container>
        <v-container fluid v-else>
          <div>
            <v-layout>
              <v-spacer/>
              <v-flex xs24>
                <searchbar v-model="search" searchBtnText='搜索用户'/>
              </v-flex>
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
                    v-else-if="item.name"
                    :key="item.uid"
                  >
                    <v-list-item-avatar>
                      <v-icon> {{ item.is_admin === "True" ? "mdi-head-flash" : "mdi-head"}}</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title>
                        <h4>
                          {{ item.name }}
                        </h4>
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        身份:
                          {{ item.is_admin === "True" ? "管理员" : "普通用户" }}
                      </v-list-item-subtitle>
                      <v-list-item-subtitle>
                        状态:
                          {{ item.blocked === "True" ? "已封禁" : "正常" }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                    
                    <v-list-item-action v-if="item.is_admin === 'True'">
                        <v-icon color="primary" @click="delete_admin(item)">
                            {{ "mdi-account-arrow-down" }}
                        </v-icon>
                    </v-list-item-action>
                    <v-list-item-action v-else>
                        <v-icon color="warning" @click="add_admin(item)">
                            {{ "mdi-account-arrow-up" }}
                        </v-icon>
                    </v-list-item-action>

                    <v-list-item-action v-if="item.blocked === 'True'">
                        <v-icon color="green" @click="delete_block(item)">
                            {{ "mdi-login" }}
                        </v-icon>
                    </v-list-item-action>
                    <v-list-item-action v-else>
                        <v-icon color="red" @click="add_block(item)">
                            {{ "mdi-block-helper" }}
                        </v-icon>
                    </v-list-item-action>
                  </v-list-item>
                </template>
              </v-list>
              <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
            </v-col>
          </div>
        </v-container>
      </div>
    </v-container>
  
</template>
  
<script>
  import searchbar from '../components/SearchBar.vue';
  export default {
    data () {
      return {
        loading: true,
        search: '',
        items: [],
        itemsPerPage: 13,
        currentPage: 1,
      }
    },
    computed: {
      filteredItems() {
        const filtered = this.items.filter(item =>
          item.name && item.name.toLowerCase().includes(this.search.toLowerCase())
        );
        return filtered;
      },
      numberOfPages () {
        return Math.ceil(this.filteredItems.length / this.itemsPerPage)
      },
      currentPageItems() {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.filteredItems.slice(startIndex, endIndex);
      },
  
    },
    mounted() {
      this.$store.commit("setAppTitle", '用户管理');
      this.getAllUsers();
    },
    
    methods: {
        getAllUsers() {
            this.$store.dispatch("showAllUsers")
            .then((res) => {
                this.items.splice(0, this.items.length, ...res.users); // 清空当前数组并插入新数据
                console.log(this.items);
            })
            .catch((e) => {
                this.$store.commit("setAlert", {
                type: "error",
                message: e,
                });
            })
            .finally(() => {
                this.loading = false;
            })
        },
        add_admin(item) {
            this.$store.dispatch("setPermission", {username: item.name, permission: 0,cancel:"false"})
            .then((res) => {
                this.$store.commit("setAlert", {
                type: "success",
                message: e,
                });
                item.is_admin = "true";
            })
            .catch((e) => {
                this.$store.commit("setAlert", {
                type: "error",
                message: e,
                });
            })
        },
        delete_admin(item) {
          this.$store.dispatch("setPermission", {username: item.name, permission: 0, cancel:"true"})
            .then((res) => {
                this.$store.commit("setAlert", {
                type: "success",
                message: e,
                });
                item.is_admin = "false";
            })
            .catch((e) => {
                this.$store.commit("setAlert", {
                type: "error",
                message: e,
                });
            })         
        },
        add_block(item) {
          this.$store.dispatch("setPermission", {username: item.name, permission: 8,cancel:"false"})
            .then((res) => {
                this.$store.commit("setAlert", {
                type: "success",
                message: e,
                });
                item.blocked = "true";
            })
            .catch((e) => {
                this.$store.commit("setAlert", {
                type: "error",
                message: e,
                });
            })
        },
        delete_block(item) {
          this.$store.dispatch("setPermission", {username: item.name, permission: 8,cancel:"true"})
            .then((res) => {
                this.$store.commit("setAlert", {
                type: "success",
                message: e,
                });
                item.blocked = "false";
            })
            .catch((e) => {
                this.$store.commit("setAlert", {
                type: "error",
                message: e,
                });
            })
        }
    },
    components: {
      searchbar
    }
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
    font-weight:900;
    top: 15px;
    right: 20px;
  }
</style>
  