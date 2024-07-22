<template>
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
                  color="primary"
                  @click="applyJoin(item)"
                > 加入 </v-btn>
              </v-list-item-action>
            </v-list-item>
          </template>
          <v-pagination v-model="currentPage" :length="numberOfPages"></v-pagination>
        </v-list>
      </v-col>
  </v-container>
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
      items: [
        { header: '所有可以加入的团队' },
        {
          name: 'Group1',
          founder: 'User1',
          description: 'Descrlines.',
          gid: 'xxx1',
          locked: true,
        },
        {
          name: 'Group2',
          founder: 'User2',
          description: 'Descrlines.',
          gid: 'xxx2',
          locked: true,
        },
        {
          name: 'Group3',
          founder: 'User3',
          description: 'Descrlines.',
          gid: 'xxx3',
          locked: false,
        },
        {
          name: 'Group4',
          founder: 'User4',
          description: 'Descrlines.',
          gid: 'xxx4',
          locked: false,
        },
        {
          name: 'Group5',
          founder: 'User5',
          description: 'Descrlines.',
          gid: 'xxx5',
          locked: false,
        },
        {
          name: 'Group6',
          founder: 'User6',
          description: 'Descrlines.',
          gid: 'xxx6',
          locked: false,
        },
        {
          name: 'Group7',
          founder: 'User7',
          description: 'Description of Group7 that is long enough to wrap onto multiple lines.',
          gid: 'xxx7',
          locked: false,
        },
        {
          name: 'Group8',
          founder: 'User8',
          description: 'Descrlines.',
          gid: 'xxx8',
          locked: false,
        },
        {
          name: 'Group9',
          founder: 'User9',
          description: 'Description of Group9 that is long enough to wrap onto multiple lines.',
          gid: 'xxx9',
          locked: false,
        },
        {
          name: 'Group10',
          founder: 'User10',
          description: 'Another description that should also wrap onto multiple lines.',
          gid: 'xxx10',
          locked: false,
        }
      ],
    }
  },
  computed: {
    numberOfPages () {
      return Math.ceil(this.filteredItems.length / this.itemsPerPage)
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
    applyJoin(item) {
      // 在这里添加处理申请加入逻辑的代码
      this.$store.commit("setAlert", {type: "success", message: `申请加入 ${item.name}`});
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