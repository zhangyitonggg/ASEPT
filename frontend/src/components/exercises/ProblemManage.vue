<template>
  <v-container fluid>
      <v-col>
        <searchbar />
      </v-col>
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
                  Tag: {{ item.tag }}
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action class="width:500px;">
                <v-btn
                  color="primary"
                  @click="changeProblem(item)"
                > 修改问题 </v-btn>
                 
                <v-btn
                  color="primary"
                  @click="addToList(item)"
                > 加入题单 </v-btn>
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
  data () {
    return {
        dialog:true,
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
        { header: '我创建的题目' },
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
        // {
        //   name: 'Group4',
        //   founder: 'User4',
        //   description: 'Descrlines.',
        //   gid: 'xxx4',
        //   locked: false,
        // },
        // { divider: true, inset: true },
        // {
        //   name: 'Group5',
        //   founder: 'User5',
        //   description: 'Descrlines.',
        //   gid: 'xxx5',
        //   locked: false,
        // },
        // { divider: true, inset: true },
        // {
        //   name: 'Group6',
        //   founder: 'User6',
        //   description: 'Descrlines.',
        //   gid: 'xxx6',
        //   locked: false,
        // },
        // { divider: true, inset: true },
        // {
        //   name: 'Group7',
        //   founder: 'User7',
        //   description: 'Description of Group7 that is long enough to wrap onto multiple lines.',
        //   gid: 'xxx7',
        //   locked: false,
        // },
        // { divider: true, inset: true },
        // {
        //   name: 'Group8',
        //   founder: 'User8',
        //   description: 'Descrlines.',
        //   gid: 'xxx8',
        //   locked: false,
        // },
        // { divider: true, inset: true },
        // {
        //   name: 'Group9',
        //   founder: 'User9',
        //   description: 'Description of Group9 that is long enough to wrap onto multiple lines.',
        //   gid: 'xxx9',
        //   locked: false,
        // },
        // { divider: true, inset: true },
        // {
        //   name: 'Group10',
        //   founder: 'User10',
        //   description: 'Another description that should also wrap onto multiple lines.',
        //   gid: 'xxx10',
        //   locked: false,
        // }
      ],
    }
  },
  computed: {
    numberOfPages () {
      return Math.ceil(this.items.length / this.itemsPerPage)
    },
    filteredKeys () {
      return this.keys.filter(key => key !== 'Name')
    },
  },
  methods: {
    nextPage () {
      if (this.page + 1 <= this.numberOfPages) this.page += 1
    },
    formerPage () {
      if (this.page - 1 >= 1) this.page -= 1
    },
    updateItemsPerPage (number) {
      this.itemsPerPage = number
    },
    changeProblem(item){
      alert('改掉这个问题！');
      //this.$router.push('/exercise/solve');
    },
    addToList(item){
      alert('选择它加入题单！');
      //this.$router.push('/exercise/solve');
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


