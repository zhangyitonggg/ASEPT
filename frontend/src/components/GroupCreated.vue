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
                v-else-if="item.name"
                :key="item.name"
              >
                <v-list-item-avatar>
                  <v-icon> {{ item.locked ? "mdi-link-lock" : "mdi-link"}}</v-icon>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>
                    <h4>
                      {{ item.name }}
                    </h4>
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Password: 
                    <strong>
                      {{ item.password }}
                    </strong>
                    <br>
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
                          v-model="curItem.name"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-checkbox
                          label="需要密码"
                          v-model="curItem.locked"
                        ></v-checkbox>
                      </v-col>
                      <v-col cols="12" v-if="curItem.locked">
                        <v-text-field
                          label="密码"
                          v-model="curItem.password"
                        ></v-text-field>
                      </v-col>
                      <template>
                        <v-container fluid>
                          <v-textarea
                            name="描述"
                            filled
                            label="描述"
                            auto-grow
                            v-model="curItem.description"
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
                    @click="submitModifyInfo"
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
                    v-model="newGroup.name"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-checkbox
                    label="需要密码"
                    v-model="newGroup.locked"
                  ></v-checkbox>
                </v-col>
                <v-col cols="12" v-if="newGroup.locked">
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
      createDialog: false,
      curItem: {},
      newGroup: {
        name: '',
        founder: '', // 可以动态获取当前用户信息
        description: '',
        password: '',
        locked: false,
        gid: '',
      },
      search: '',
      items: [
        { header: '您创建的所有团队' },
        {
          name: 'Group1',
          founder: 'User1',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx1',
          locked: true,
        },
        {
          name: 'Group2',
          founder: 'User2',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx2',
          locked: true,
        },
        {
          name: 'Group3',
          founder: 'User3',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx3',
          locked: false,
        },
        {
          name: 'Group4',
          founder: 'User4',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx4',
          locked: false,
        },
        {
          name: 'Group5',
          founder: 'User5',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx5',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group6',
          founder: 'User6',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx6',
          locked: false,
        },
      ],
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
  methods: {
    getCreatedGroups() {
      this.$store
        .dispatch("showCreatedGroups")
        .then((res) => {
          this.temp = []
          this.temp = res.groups;
          this.temp.unshift({ header: '您创建的所有团队' });
          this.items = this.temp;
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
      this.curItem = item;
      this.dialog = true;
    },
    submitModifyInfo() { // todo
      this.dialog = false;
      console.log(this.curItem);
    },
    handleAboutClick(flag) {
      console.log(flag);  
      this.dialog = false
      if (flag) {
        alert(`你选择了离开 ${this.curItem.name}`);
        // 使用 splice 方法从 items 中移除 curItem
        const index = this.items.findIndex(item => item.gid === this.curItem.gid);
        if (index !== -1) {
          this.items.splice(index, 1);
        }
      }
    },
    submitNewGroup() {
      // 为新群聊生成一个唯一的gid
      this.newGroup.gid = 'gid-' + Date.now(); // todo
      this.newGroup.founder = this.$store.getters.username; // 可以动态获取当前用户信息
      this.items.push({ ...this.newGroup }); 
      this.createDialog = false;
      // 重置 newGroup
      this.newGroup = {
        name: '',
        founder: '当前用户',
        description: '',
        password: '',
        locked: false,
        gid: '',
      };
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
