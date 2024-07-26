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
        <v-spacer/>
        <searchbar v-model="search" searchBtnText='搜索团队'/>
      </v-layout>
      <v-col v-if="items.length == 0" class="d-flex justify-center">
        <h2>
          暂时没有你可以加入的团队。
        </h2>
      </v-col>
      <v-col v-else>
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
              :key="item.gid"
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
                  Description:
                  {{ item.description }}
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn
                  color="primary"
                  @click="applyJoin(item)"
                > 加入 </v-btn>
              </v-list-item-action>
            </v-list-item>
          </template>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-list>
      </v-col>
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title>
            <span class="headline">输入密码</span>
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="password" label="密码" type="password"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog = false">取消</v-btn>
            <v-btn color="blue darken-1" text @click="confirmJoin">确认</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script>
import searchbar from './SearchBar.vue'

export default {
  data () {
    return {
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      currentPage: 1,
      itemsPerPage: 13,
      loading: true,
      items: [],
      dialog: false,
      selectedItem: null,
      password: '',
    }
  },
  mounted() {
    this.getUnGroups();
  },
  computed: {
    numberOfPages () {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage)
    },
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.group_name && item.group_name.toLowerCase().includes(this.search.toLowerCase())
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
    getUnGroups() {
      this.$store.dispatch("showUnGroups")
        .then((res) => {
          this.items.splice(0, this.items.length, ...res.groups);
          console.log('@',this.items);
        })
        .catch((e) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: e,
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    applyJoin(item) {
      if (item.need_password) {
        this.selectedItem = item;
        this.dialog = true;
      } else {
        this.selectedItem = item;
        this.password = "";
        this.confirmJoin();
      }
    },
    confirmJoin() {
      this.dialog = false;
      this.$store
        .dispatch("joinGroup", { gid: this.selectedItem.gid, password: this.password })
        .then((res) => {
          this.$store.commit("setAlert", {
            type: "success",
            message: `加入 ${this.selectedItem.group_name} 成功`,
          });
        })
        .catch((e) => {
          this.$store.commit("setAlert", {
            type: "error",
            message: e,
          });
        })
        .finally(() => {
          this.getUnGroups();
          this.password = '';
          this.selectedItem = null;
        });
    },
  },
  components: {
    searchbar
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
