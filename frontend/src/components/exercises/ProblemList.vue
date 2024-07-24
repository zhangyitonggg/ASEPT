<template>
  <v-container fluid>
    <v-col>
      <v-list three-line>
        <template v-for="(item, index) in items">
          <v-subheader
            v-if="item.header"
            :key="item.header"
            v-text="item.header"
          ></v-subheader>
          <v-divider
            v-else-if="item.divider"
            :key="index"
            :inset="item.inset"
          ></v-divider>
          <v-list-item v-else-if="item.pgid" :key="item.pgid">
            <v-list-item-avatar>
              <v-icon> mdi-invoice-list-outline</v-icon>
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
              <v-btn color="primary" @click="openDialog(item)">查看题单</v-btn>
            </v-list-item-action>
          </v-list-item>
        </template>
      </v-list>
    </v-col>

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          题单详情
          <v-spacer></v-spacer>
          <v-btn icon @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-subtitle>
          题单名称: {{ currentItem.name }}
        </v-card-subtitle>

        <v-card-text>
          <v-row>
            <v-col v-for="(problem, index) in currentItem.problems" :key="index" cols="12" md="4">
              <v-card class="mb-4">
                <v-card-title>
                  题目 {{ index + 1 }}
                </v-card-title>
                <v-card-subtitle>
                  Tag: {{ problem.tag }}
                </v-card-subtitle>
                <v-card-text>
                  {{ problem.description }}
                </v-card-text>
                <v-card-actions>
                  <v-btn color="primary" @click="startProblem(problem)">去做题</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="dialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      currentItem: { name: '', tag: '', content: '' },
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 4,
      sortBy: 'name',
      keys: ['Name', 'Tag'],
      items: [],
    };
  },
  created() {
    this.fetchItems();
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
    filteredKeys() {
      return this.keys.filter((key) => key !== 'Name');
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
    openDialog(item) {
      this.currentItem = item;
      this.dialog = true;
    },
    startProblem(problem) {
      this.$router.push({ path: 'solve', append: true });
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
