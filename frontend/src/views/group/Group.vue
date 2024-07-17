<template>
    <div>
        <div>
            <Header></Header>
        </div>
        <div class="group-container">
        <!-- 左半边：我的群组和退出群组 -->
        <div class="left-pane">
            <h2>我的群组</h2>
            <div v-if="userGroups.length > 0">
            <ul>
                <li v-for="group in userGroups" :key="group.name">
                <span>{{ group.name }}</span>
                <button @click="leaveGroup(group.name)">退出</button>
                </li>
            </ul>
            </div>
        </div>
        
        <!-- 右半边：创建群组和搜索群组 -->
        <div class="right-pane">
            <!-- 创建群组 -->
            <div>
            <h2>创建群组</h2>
            <input v-model="newGroupName" placeholder="输入群组名称">
            <button @click="createGroup">创建</button>
            </div>

            <!-- 搜索群组 -->
            <h2>搜索群组</h2>
            <input v-model="searchQuery" placeholder="搜索群组" @input="searchGroups">
            <div v-if="groups.length > 0">
            <h2>搜索结果</h2>
            <ul>
                <li v-for="group in groups" :key="group.name">
                <span>{{ group.name }}</span>
                <button @click="joinGroup(group)" v-if="!isUserInGroup(group.name)">加入</button>
                <button @click="leaveGroup(group.name)" v-if="isUserInGroup(group.name)">退出</button>
                </li>
            </ul>
            </div>
        </div>
        </div>
    </div>
</template>
  
<script>
  import axios from 'axios';
  import Header from '../../components/Header.vue'
  
  export default {
    name: 'Group',
    data() {
      return {
        searchQuery: '',
        newGroupName: '',
        groups: [],
        userGroups: []
      };
    },
    components: {
      Header
    },
    methods: {
      searchGroups() {
        axios.get(`/api/groups?query=${this.searchQuery}`)
          .then(response => {
            this.groups = response.data;
          })
          .catch(error => {
            console.error('Error searching groups:', error);
          });
      },
      joinGroup(group) {
        axios.post('/api/groups/join', { groupName: group.name })
          .then(() => {
            this.userGroups.push(group);
          })
          .catch(error => {
            console.error('Error joining group:', error);
          });
      },
      createGroup() {
        if (!this.newGroupName) {
            alert('请输入群组名称');
            return;
        }
        axios.post('/api/groups', { groupName: this.newGroupName })
            .then(response => {
            this.userGroups.push(response.data); // 假设响应中返回新创建的群组信息
            this.newGroupName = ''; // 清空输入框
            })
            .catch(error => {
            console.error('Error creating group:', error);
            });
        },
      leaveGroup(groupName) {
        axios.post('/api/groups/leave', { groupName })
          .then(() => {
            this.userGroups = this.userGroups.filter(group => group.name !== groupName);
          })
          .catch(error => {
            console.error('Error leaving group:', error);
          });
      },
      isUserInGroup(groupName) {
        return this.userGroups.some(group => group.name === groupName);
      }
    }
  };
</script>
  
<style scoped>
.group-container {
  display: flex;
  justify-content: space-between;
}

.left-pane, .right-pane {
  width: 48%;
}

h1, h2 {
  color: #333;
}

input {
  display: block;
  margin-bottom: 20px;
  padding: 10px;
  width: 100%;
  box-sizing: border-box;
}

button {
  margin-left: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #007bff;
  color: white;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
}
</style>