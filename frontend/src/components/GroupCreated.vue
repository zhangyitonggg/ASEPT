<template>
  <div>
    <v-container fluid>
        <v-col>
          <searchbar v-model="search"/>
        </v-col>
        <v-col>
          <v-list three-line>
            <template v-for="(item, index) in filteredItems">
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
        { divider: true, inset: true },
        {
          name: 'Group2',
          founder: 'User2',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx2',
          locked: true,
        },
        { divider: true, inset: true },
        {
          name: 'Group3',
          founder: 'User3',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx3',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group4',
          founder: 'User4',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx4',
          locked: false,
        },
        { divider: true, inset: true },
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
        { divider: true, inset: true },
        {
          name: 'Group7',
          founder: 'User7',
          description: 'Description of Group7 that is long enough to wrap onto multiple lines.',
          password: "pwd",
          gid: 'xxx7',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group8',
          founder: 'User8',
          description: 'Descrlines.',
          password: "pwd",
          gid: 'xxx8',
          locked: false,
        },
        { divider: true, inset: true },
        {
          name: 'Group9',
          founder: 'User9',
          description: 'Description of Group9 that is long enough to wrap onto multiple lines.',
          password: "pwd",
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
    filteredItems() {
      const filtered = this.items.filter(item =>
        item.name && item.name.toLowerCase().includes(this.search.toLowerCase())
      );
      // console.log('Filtered Items:', filtered); // 调试输出
      return filtered;
    }
  },
  methods: {
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