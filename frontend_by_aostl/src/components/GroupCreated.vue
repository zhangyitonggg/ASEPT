<template>
  <div>
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
                    color="warning"
                    @click="leave(item)"
                  > 离开 </v-btn>
                </v-list-item-action>

              </v-list-item>
            </template>
          </v-list>
        </v-col>
    </v-container>
    <v-row justify="center">
      <v-dialog
        v-model="dialog"
        max-width="290"
      >
        <v-card>
          <v-card-title class="text-h7">
            确定要离开 {{curItem.name}} 吗？
          </v-card-title>

           <v-card-actions>
            <v-spacer></v-spacer>
  
            <v-btn
              color="green darken-1"
              text
              @click="handleAboutClick(false)"
            >
              取消
            </v-btn>
  
            <v-btn
              color="red darken-1"
              text
              @click="handleAboutClick(true)"
            >
              确定
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
      itemsPerPageArray: [4, 8, 12],
      dialog: false,
      curItem: {},
      search: '',
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 4,
      sortBy: 'name',
      keys: [
        'Name',
        'description',
      ],
      items: [
        { header: '所有可以加入的团队' },
        {
          name: 'Group1',
          founder: 'User1',
          description: 'Descrlines.',
          gid: 'xxx1',
          locked: true,
        },
        { divider: true, inset: true },
        {
          name: 'Group2',
          founder: 'User2',
          description: 'Descrlines.',
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
        { divider: true, inset: true },
        {
          name: 'Group5',
          founder: 'User5',
          description: 'Descrlines.',
          gid: 'xxx5',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group6',
          founder: 'User6',
          description: 'Descrlines.',
          gid: 'xxx6',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group7',
          founder: 'User7',
          description: 'Description of Group7 that is long enough to wrap onto multiple lines.',
          gid: 'xxx7',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group8',
          founder: 'User8',
          description: 'Descrlines.',
          gid: 'xxx8',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group9',
          founder: 'User9',
          description: 'Description of Group9 that is long enough to wrap onto multiple lines.',
          gid: 'xxx9',
          locked: false,
        },
        { divider: true, inset: true },
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
    leave(item) {
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









<!-- <template>
  <div class="container">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card class="custom-card">
            <v-card-title class="fixed-header"><span style="margin-bottom: 5px;">我创建的群组</span>
              <v-spacer></v-spacer>
              <v-btn small color="primary" class="create" @click="createGroup">
                创建群组
              </v-btn>
            </v-card-title>

            <v-card-subtitle class="custom-card-subtitle">
              <v-expansion-panels v-model="activePanel" class="custom-collapse">
                <v-expansion-panel
                  v-for="group in groupCreated"
                  :key="group.gid"
                  class="custom-collapse-item"
                >
                  <v-expansion-panel-header class="custom-collapse-item__header">
                    {{ group.group_name }}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content class="custom-collapse-item__content">
                    <div class="description">{{ group.description }}</div>
                    <div class="password">密码: {{ group.password }}</div>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activePanel: [0],
      groupCreated: [
        {
          group_name: "计组学习小组",
          password: "password1",
          gid: "xxx1",
          description: "Description of group1"
        },
        {
          group_name: "今天我是大卷王",
          password: "password2",
          gid: "xxx2",
          description: "Description of group2"
        },
        {
          group_name: "前端学习小组",
          password: "password3",
          gid: "xxx3",
          description: "Description of group3"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx4",
          description: "Description of group4"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx5",
          description: "Description of group4"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx6",
          description: "Description of group4"
        },
        {
          group_name: "后端学习小组",
          password: "password4",
          gid: "xxx7",
          description: "Description of group4"
        },
      ]
    };
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 45%
}

.fixed-header {
  background-color: #36a492;
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
}

.custom-card {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.custom-card-subtitle {
  padding: 7px;
  background: linear-gradient(135deg, #f3f4f7, #fff);
}

.custom-collapse {
  border: 1px solid #ccc;
  overflow-y: auto;
  max-height: 275px;
  background: #fafafa;
}

.custom-collapse-item {
  overflow: hidden;
  margin-bottom: 10px;
  background: none;
  transition: transform 0.3s, box-shadow 0.3s;
}

.custom-collapse-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.custom-collapse-item__header {
  background: linear-gradient(135deg, #57d59c, #36a492);
  color: #fff;
  border-radius: 8px 8px 0 0;
  padding: 10px;
}

.custom-collapse-item__header:hover {
  background: linear-gradient(135deg, #2c8e7d, #42b983);
}

.custom-collapse-item__content {
  border-radius: 0 0 8px 8px;
  padding: 10px;
  background: linear-gradient(135deg, #2c8e7d, #42b983);
}

.description {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.password {
  font-size: 17px;
  font-weight: bold;
  color: #ff6f61;
}

.create {
  background: rgb(57, 48, 185);
  color: white;
  border: none;
  border-radius: 2px;
  padding: 8px 16px;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-bottom: 5px;
}

.create:hover {
  background: linear-gradient(135deg, #44ded1, #1179f1);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.create:focus {
  outline: none;
}

</style> -->
