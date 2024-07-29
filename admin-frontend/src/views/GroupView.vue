<template>
  <v-container>
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
                海内存知己，天涯若比邻。
              </h3>
              <span>正在获取你所管理的团队。</span>
            </v-col>
          </v-row>
        </v-container>
      </template>
      <v-container fluid v-else>
        <template v-if="items.length == 0">
          <v-btn color="success" @click="openCreateDialog">创建团队</v-btn>
          <v-col class="d-flex justify-center align-center">
            <h2>
              没有你可以管理的团队。试着创建一个？
            </h2>
          </v-col>
        </template>
        <div v-else>
          <v-layout>
            <v-flex xs1>
              <v-btn color="success" @click="openCreateDialog">创建团队</v-btn>
            </v-flex>
            <v-spacer />
            <v-flex xs24>
              <searchbar v-model="search" searchBtnText='搜索团队' />
            </v-flex>
          </v-layout>
          <v-col>
            <v-list three-line>
              <template v-for="(item, index) in currentPageItems">
                <v-divider inset></v-divider>
                <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>
                <v-list-item v-else-if="item.name" :key="item.gid">
                  <v-list-item-avatar>
                    <v-icon> {{ item.is_open ? "mdi-link-lock" : "mdi-link" }}</v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>
                      <h4>
                        {{ item.name }}
                      </h4>
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      Founder:
                      {{ item.owner }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                      Description:
                      {{ item.description }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn color="secondary" @click="init_modified_group(item)"> 管理 </v-btn>
                  </v-list-item-action>
                  <v-list-item-action>
                    <v-btn color="error" @click="delete_group(item)"> 解散 </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </template>
            </v-list>
            <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
          </v-col>
        </div>
      </v-container>
      <v-row justify="center">
        <v-dialog v-model="dialog" max-width="50%">
          <v-card>
            <v-card-title>
              修改团队信息
            </v-card-title>
            <v-card-text>
              <v-text-field label="群名" required filled v-model="modified_group.name"></v-text-field>
              <v-textarea name="描述" filled label="描述" auto-grow v-model="modified_group.description"></v-textarea>
              <v-switch v-model="modified_group.is_open">
                <template v-slot:label>加入需要密码：{{ `${modified_group.is_open ? '是' : '否'}` }}</template>
              </v-switch>
              <template v-if="modified_group.is_open">
                <v-text-field label="修改密码" v-model="modified_group.password" hint="可选，留空则不修改密码。" :rules="[
                  v => !!v || '',
                  v => v == null,
                  v => v.length > 8 || '至少9字符',
                  v => v.length < 21 || '至多20字符',
                  v => {
                    const pattern = /^.*[0-9].*$/
                    const pattern_w = /^.*[a-zA-Z].*$/
                    return (
                      (pattern.test(v) && pattern_w.test(v)) || '必须包含数字和字母'
                    )
                  }
                ]" type="password" persistent-hint></v-text-field>
              </template>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" text @click.stop="submitModifyInfo"> 保存 </v-btn>
              <v-btn color="error" text @click="dialog = false"> 取消 </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="createDialog" max-width="50%">
          <v-card>
            <v-card-title>
              <span class="text-h5">创建团队</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12">
                    <v-text-field label="群名*" required v-model="newGroup.name"></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-checkbox label="需要密码" v-model="newGroup.is_open"></v-checkbox>
                  </v-col>
                  <v-col cols="12" v-if="newGroup.is_open">
                    <v-text-field label="密码" v-model="newGroup.password"></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-textarea label="描述" required auto-grow v-model="newGroup.description"></v-textarea>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-btn color="blue darken-1" text @click="createDialog = false">
                取消
              </v-btn>
              <v-btn color="blue darken-1" text @click="submitNewGroup">
                创建
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </div>
  </v-container>

</template>

<script>
import searchbar from '../components/SearchBar.vue';
export default {
  name: 'GroupView',
  data() {
    return {
      loading: true,
      dialog: false,
      changePassword: false,
      createDialog: false,
      modified_group: {
        name: '',
        description: '',
        password: '',
        is_open: false,
        gid: '',
      },
      newGroup: {
        name: '',
        description: '',
        password: '',
        is_open: false,
        gid: '',
      },
      search: '',
      items: [],
      itemsPerPage: 13,
      currentPage: 1,
    }
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
  computed: {
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.name && item.name.toLowerCase().includes(this.search.toLowerCase())
      );
      return filtered;
    },
    numberOfPages() {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage)
    },
    currentPageItems() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      return this.filteredItems.slice(startIndex, endIndex);
    },

  },
  mounted() {
    this.$store.commit("setAppTitle", '团队管理');
    this.getCreatedGroups();
  },

  methods: {
    getCreatedGroups() {
      this.$store.dispatch("showJoinedGroups")
        .then((res) => {
          res.groups.forEach(group => {
            group.name = group.group_name;
          });
          this.items.splice(0, this.items.length, ...res.groups); // 清空当前数组并插入新数据
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
    openCreateDialog() {
      this.createDialog = true;
    },
    init_modified_group(item) {
      this.modified_group = {
        gid: item.gid,
        name: item.name,
        description: item.description,
        password: "",
        is_open: item.is_open
      };
      this.changePassword = false;
      this.dialog = true;
    },
    delete_group(item) {
      console.log(item);
      this.$store.dispatch('deleteGroup', { gid: item.gid })
        .then(() => {
          this.$store.commit("setAlert", { type: "success", message: `解散团队 ${item.group_name} 成功。` });
          this.getCreatedGroups();
        })
        .catch((e) => {
          this.$store.commit("setAlert", { type: "error", message: e });
        });
    },
    submitModifyInfo() {
      let password = this.modified_group.password;
      if (this.modified_group.is_open === false) {
        password = "";
      } else if (this.modified_group.password === "") {
        password = null;
      }
      this.$store.dispatch('modifyGroup', {
        gid: this.modified_group.gid,
        group_name: this.modified_group.name,
        description: this.modified_group.description,
        password: password
      })
        .then(() => {
          this.$store.commit("setAlert", { type: "success", message: `修改团队 ${this.modified_group.name} 信息成功。` });
          this.getCreatedGroups();
        })
        .catch((e) => {
          this.$store.commit("setAlert", { type: "error", message: e });
        })
        .finally(() => {
          this.tempItem = {};
          this.curItem = {};
        });
      this.dialog = false;
    },
    submitNewGroup() {
      this.createDialog = false;
      this.$store
        .dispatch('createGroup', { group_name: this.newGroup.name, description: this.newGroup.description, password: this.newGroup.password })
        .then((res) => {
          this.$store.commit("setAlert", { type: "success", message: `创建 ${this.newGroup.name} 成功` });
          this.getCreatedGroups();
        })
        .catch((e) => {
          this.$store.commit("setAlert", { type: "error", message: e });
        })
        .finally(() => {
          this.newGroup = {
            name: '',
            description: '',
            password: '',
            is_open: false,
            gid: '',
          };
        });
    },
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
