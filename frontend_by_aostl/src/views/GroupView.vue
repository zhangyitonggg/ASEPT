<template>
  <div>
      <div class="group-container">
        <!-- 左半边：我创建的群组和我的群组 -->
        <div class="left-pane">
          <GroupCreated />
          <GroupAdded />
          <!-- 你的群组内容 -->
        </div>
        
        <!-- 右半边：创建群组和搜索群组 -->
        <div class="right-pane">
          <EnterGroup />
        </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import EnterGroup from '@/components/EnterGroup.vue';
import GroupAdded from '@/components/GroupAdded.vue';
import GroupCreated from '@/components/GroupCreated.vue';
export default {
  name: 'GroupView',    
  data() {
    return {
    };
  },
  components: {
    EnterGroup,
    GroupAdded,
    GroupCreated
  },
  methods: {

  }
};
</script>

<style scoped>
.group-container {
display: flex;
justify-content: center; /* 将子项在主轴上居中对齐 */
align-items: center; /* 将子项在交叉轴上居中对齐 */
height: 100vh; /* 使容器高度为视口高度 */
}

.left-pane, .right-pane {
width: 48%;
height:90%;
margin-left: 0.5%;
margin-right: 0.5%;
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
