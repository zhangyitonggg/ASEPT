<template>
  <div>
    <v-container fluid>
      <v-layout>
        <v-flex xs1>
           <v-btn color="success" @click="openCreateDialog">新建群聊</v-btn>
        </v-flex>
        <v-spacer/>
        <v-flex xs24>
          <searchbar v-model="search" searchBtnText='搜索团队'/>
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
                    Description:
                      {{ item.description }}
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-btn
                    color="secondary"
                    @click="manage(item)"
                  > 管理 </v-btn>
                </v-list-item-action>
              </v-list-item>
            </template>
          </v-list>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-col>
    </v-container>
    <v-row justify="center">
      <v-dialog
        v-model="dialog"
        max-width="290"
      >
        <template>
          <v-row justify="center">
            <v-dialog
              v-model="dialog"
              persistent
              max-width="600px"
            > 
              <v-card>
                <v-card-title>
                  <span class="text-h5">修改{{curItem.name}}信息</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          label="群名"
                          required
                          v-model="tempItem.group_name"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-checkbox
                          label="取消密码"
                          v-if="curItem.need_password && !changePassword"
                          @change="tempItem.need_password = !tempItem.need_password"
                        ></v-checkbox>
                        <v-checkbox
                          label="设置密码"
                          v-if="!curItem.need_password"
                          v-model="changePassword"
                        ></v-checkbox>
                        <v-checkbox
                          label="修改密码"
                          v-if="curItem.need_password && tempItem.need_password"
                          v-model="changePassword"
                        ></v-checkbox>
                        <v-text-field
                          label="密码"
                          v-if="changePassword"
                          v-model="tempItem.password"
                        ></v-text-field>
                      </v-col>
                      <template>
                        <v-container fluid>
                          <v-textarea
                            name="描述"
                            filled
                            label="描述"
                            auto-grow
                            v-model="tempItem.description"
                          ></v-textarea>
                        </v-container>
                      </template>
                    </v-row>
                  </v-container>
                  <small>*indicates required field</small>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                  color="blue darken-1"
                  text
                  @click="submitModifyInfo(false)"
                >
                  Cancel
                </v-btn>
                  <v-btn
                    color="warning"
                    text
                    @click="submitModifyInfo(true)"
                  >
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </template>
      </v-dialog>
      <v-dialog
        v-model="createDialog"
        persistent
        max-width="600px"
      > 
        <v-card>
          <v-card-title>
            <span class="text-h5">新建群聊</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    label="群名*"
                    required
                    v-model="newGroup.group_name"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-checkbox
                    label="需要密码"
                    v-model="newGroup.need_password"
                  ></v-checkbox>
                </v-col>
                <v-col cols="12" v-if="newGroup.need_password">
                  <v-text-field
                    label="密码"
                    v-model="newGroup.password"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    label="描述"
                    required
                    auto-grow
                    v-model="newGroup.description"
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="blue darken-1"
              text
              @click="createDialog = false"
            >
              取消
            </v-btn>
            <v-btn
              color="blue darken-1"
              text
              @click="submitNewGroup"
            >
              创建
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
      changePassword: false,
      createDialog: false,
      curItem: {},
      tempItem: {},
      newGroup: {
        group_name: '',
        description: '',
        password: '',
        need_password: false,
        gid: '',
      },
      search: '',
      items: [],
      itemsPerPage: 13,
      currentPage: 1,
    }
  },
  computed: {
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.group_name && item.group_name.toLowerCase().includes(this.search.toLowerCase())
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
    this.getCreatedGroups();
  },
  methods: {
    getCreatedGroups() {
      this.$store
        .dispatch("showCreatedGroups")
        .then((res) => {
          this.items.splice(0, this.items.length, { header: '您创建的所有团队' }, ...res.groups); // 清空当前数组并插入新数据
          console.log(this.items);
        })
        .catch((e) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: e,
          });
        });
    },
    openCreateDialog() {
      this.createDialog = true;
    },
    manage(item) {
      this.curItem = {gid: item.gid, group_name: item.group_name, description: item.description, password: null, need_password: item.need_password};
      this.tempItem = {gid: item.gid, group_name: item.group_name, description: item.description, password: null, need_password: item.need_password};
      this.dialog = true;
      this.changePassword = false;
    },
    submitModifyInfo(flag) {
      this.dialog = false;
      console.log('@',this.curItem);
      console.log('#',this.tempItem);
      if (!flag) {
        this.tempItem = {};
        return;
      }
      if (!this.changePassword) {
        this.tempItem.password = null;
        if (!this.tempItem.need_password) {
          this.tempItem.password = "";
        }
      }
      console.log('!',this.tempItem);
      this.$store
        .dispatch('modifyGroup', {gid: this.tempItem.gid, group_name: this.tempItem.group_name, description: this.tempItem.description, password: this.tempItem.password})
        .then((res) => {
          this.$store.commit("setAlert", {type: "success", message: `修改 ${this.curItem.group_name} 信息成功`});
          this.getCreatedGroups();
        })
        .catch((e) => {
          this.$store.commit("setAlert", {type: "error", message: e});
        })
        .finally(() => {
          this.tempItem = {};
          this.curItem = {};
        });
    },
    submitNewGroup() {
      this.createDialog = false;
      this.$store
      .dispatch('createGroup', {group_name: this.newGroup.group_name, description: this.newGroup.description, password: this.newGroup.password})
      .then((res) => {
        this.$store.commit("setAlert", {type: "success", message: `创建 ${this.newGroup.group_name} 成功`});
        this.getCreatedGroups();
      })
      .catch((e) => {
        this.$store.commit("setAlert", {type: "error", message: e});
      })
      .finally(() => {
        this.newGroup = {
          group_name: '',
          description: '',
          password: '',
          need_password: false,
          gid: '',
        };
      });
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
