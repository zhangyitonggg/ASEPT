<template>
  <v-container fluid>
    <v-col>
      <v-card class="mb-5">
        <v-card-title>
          题目列表名称: {{ listName }}
        </v-card-title>
        <v-card-subtitle>
          题目数量: {{ items.length }}
        </v-card-subtitle>
      </v-card>
    </v-col>
    <v-row class="align-center">
      <v-col cols="auto">
        <v-btn class="fixed-button" fab dark color="indigo" @click="returnback">
          <v-icon dark>
            mdi-arrow-u-left-bottom-bold
          </v-icon>
        </v-btn>
      </v-col>
      <v-col>
        <searchbar />
      </v-col>
    </v-row>
    <v-col>
      <v-list three-line>
        <template v-for="(item, index) in items">
          <v-subheader v-if="item.header" :key="item.header" v-text="item.header"></v-subheader>
          <v-divider v-else-if="item.divider" :key="index" :inset="item.inset"></v-divider>
          <v-list-item v-else-if="item.name" :key="item.name">
            <v-list-item-avatar>
              <v-icon> mdi-help-circle-outline</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                <h4>
                  {{ item.name }}
                </h4>
              </v-list-item-title>
              <v-list-item-subtitle>
                Tag: {{ item.tag }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn color="primary" @click="solveProblem(item)"> 去做题 </v-btn>
            </v-list-item-action>

          </v-list-item>
        </template>
      </v-list>
    </v-col>
  </v-container>
</template>

<script>
import searchbar from '../SearchBar.vue'

export default {
  data() {
    return {
      itemsPerPageArray: [4, 8, 12],
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 4,
      sortBy: 'name',
      keys: [
        'Name',
        'Tag',
      ],
      items: [
        { header: '题目列表' },
        {
          name: 'Problem1',
          tag: 'Descrlines.',
          gid: 'xxx1',
          locked: true,
          content: '66666666',
        },
        { divider: true, inset: true },
        {
          name: 'Group2',
          //founder: 'User2',
          tag: 'Descrlines.',
          gid: 'xxx2',
          locked: true,
        },
        { divider: true, inset: true },
        {
          name: 'Group3',
          founder: 'User3',
          description: 'Descrlines.',
          gid: 'xxx3',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group4',
          founder: 'User4',
          description: 'Descrlines.',
          gid: 'xxx4',
          locked: false,
        },
      ],
    }
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.items.length / this.itemsPerPage)
    },
    filteredKeys() {
      return this.keys.filter(key => key !== 'Name')
    },
  },
  methods: {
    nextPage() {
      if (this.page + 1 <= this.numberOfPages) this.page += 1
    },
    formerPage() {
      if (this.page - 1 >= 1) this.page -= 1
    },
    updateItemsPerPage(number) {
      this.itemsPerPage = number
    },
    solveProblem(item) {
      this.$router.push({ path: 'solve', append: true });
    },
    returnback() {
      this.$router.go(-1);
    }
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
