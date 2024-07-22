<template>
  <div>
    <v-container fluid>
        <v-col>
          <searchbar v-model="search" searchBtnText='搜索团队'/>
        </v-col>
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
                          label="Group Name*"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          label="Password(可选)"
                          type="password"
                          required
                        ></v-text-field>
                      </v-col>
           
                      <template>
                        <v-container fluid>
                          <v-textarea
                            name="description"
                            filled
                            label="Group Description*"
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
                    @click="dialog = false"
                  >
                    Close
                  </v-btn>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="dialog = false"
                  >
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-row>
        </template>
        <!--  -->

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
      items: [
        { header: '您加入的所有团队' },
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
    manage(item) {
      this.curItem = item;
      this.dialog = true;
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