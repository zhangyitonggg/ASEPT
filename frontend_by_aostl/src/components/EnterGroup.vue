<template>
  <div class="scrollable-container">
    <v-container fluid>
      <v-data-iterator
        :items="items"
        :items-per-page.sync="itemsPerPage"
        :page.sync="page"
        :search="search"
        :sort-by="sortBy.toLowerCase()"
        :sort-desc="sortDesc"
        hide-default-footer
      >
        <template v-slot:header>
          <v-toolbar
            dark
            color="blue darken-3"
            class="mb-1"
          >
            <span class="header-title">所有群聊</span>
            <v-text-field
              v-model="search"
              clearable
              flat
              solo-inverted
              hide-details
              prepend-inner-icon="mdi-magnify"
              label="Search"
            ></v-text-field>
            <template v-if="$vuetify.breakpoint.mdAndUp">
              <v-spacer></v-spacer>
              <v-select
                v-model="sortBy"
                flat
                solo-inverted
                hide-details
                :items="keys"
                prepend-inner-icon="mdi-magnify"
                label="Sort by"
              ></v-select>
              <v-spacer></v-spacer>
            </template>
          </v-toolbar>
        </template>
  
        <template v-slot:default="props">
          <v-row>
            <v-col
              v-for="item in props.items"
              :key="item.gid"
              cols="12"
              sm="6"
            >
              <v-card class="item-card">
                <v-card-title class="subheading font-weight-bold">
                  {{ item.name }}
                  <v-spacer></v-spacer>
                  <v-btn small color="primary" class="apply-button" @click="applyJoin(item)">
                    申请加入
                  </v-btn>
                </v-card-title>
  
                <v-divider></v-divider>
  
                <v-list dense>
                  <v-list-item
                    v-for="(key, index) in filteredKeys"
                    :key="index"
                  >
                    <v-list-item-content :class="{ 'blue--text': sortBy === key }">
                      {{ key }}:
                    </v-list-item-content>
                    <v-list-item-content
                      class="align-end"
                      :class="{ 'blue--text': sortBy === key }"
                    >
                      <span class="description-text">
                        {{ item[key.toLowerCase()] }}
                      </span>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-col>
          </v-row>
        </template>
  
        <template v-slot:footer>
          <v-row
            class="mt-2"
            align="center"
            justify="center"
          >
            <span
              class="pagination-info mr-4 grey--text"
            >
              Page {{ page }} of {{ numberOfPages }}
            </span>
            <v-spacer></v-spacer>
            <v-btn
              fab
              dark
              color="blue darken-3"
              class="mr-1"
              @click="formerPage"
            >
              <v-icon>mdi-chevron-left</v-icon>
            </v-btn>
            <v-btn
              fab
              dark
              color="blue darken-3"
              class="ml-1"
              @click="nextPage"
            >
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-row>
        </template>
      </v-data-iterator>
    </v-container>
  </div>
</template>

<script>
  export default {
    name: 'EnterGroup',
    data () {
      return {
        itemsPerPageArray: [4, 8, 12],
        search: '',
        filter: {},
        sortDesc: false,
        page: 1,
        itemsPerPage: 8,
        sortBy: 'name',
        keys: [
          'Name',
          'description',
        ],
        items: [
          {
            name: 'Group1',
            founder: 'User1',
            description: 'Descrlines.',
            gid: 'xxx1',
          },
          {
            name: 'Group2',
            founder: 'User2',
            description: 'Descrlines.',
            gid: 'xxx2',
          },
          {
            name: 'Group3',
            founder: 'User3',
            description: 'Descrlines.',
            gid: 'xxx3',
          },
          {
            name: 'Group4',
            founder: 'User4',
            description: 'Descrlines.',
            gid: 'xxx4',
          },
          {
            name: 'Group5',
            founder: 'User5',
            description: 'Descrlines.',
            gid: 'xxx5',
          },
          {
            name: 'Group6',
            founder: 'User6',
            description: 'Descrlines.',
            gid: 'xxx6',
          },
          {
            name: 'Group7',
            founder: 'User7',
            description: 'Description of Group7 that is long enough to wrap onto multiple lines.',
            gid: 'xxx7',
          },
          {
            name: 'Group8',
            founder: 'User8',
            description: 'Descrlines.',
            gid: 'xxx8',
          },
          {
            name: 'Group9',
            founder: 'User9',
            description: 'Description of Group9 that is long enough to wrap onto multiple lines.',
            gid: 'xxx9',
          },
          {
            name: 'Group10',
            founder: 'User10',
            description: 'Another description that should also wrap onto multiple lines.',
            gid: 'xxx10',
          }
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
      applyJoin(item) {
        // 在这里添加处理申请加入逻辑的代码
        alert(`申请加入 ${item.name}`);
      },
    },
  }
</script>

<style scoped>
.scrollable-container {
  height: 100vh;
  overflow: auto;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
  margin-right: 10%;
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
  position: absolute;
  top: 8px;
  right: 18px;
}
</style>
