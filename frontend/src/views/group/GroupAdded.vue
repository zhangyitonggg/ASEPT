<!-- <template>
    <div class="container">
      <el-scrollbar class="scroll-box">
        <el-card
          v-for="group in groupAdded"
          :key="group.gid"
          class="item"
          shadow="hover"
        >
          <div class="card-content">
            <div class="group-info">
              <div class="group-details">
                <div class="group-name">{{ group.group_name }}</div>
                <div class="group-description">{{ group.description }}</div>
              </div>
              <div class="edit-button-container">
                <el-button type="text" class="edit-button" @click="leaveGroup(group)">退出</el-button>
              </div>
            </div>
          </div>
        </el-card>
      </el-scrollbar>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
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
        ],
      };
    },
    methods: {

    },
    mounted() {
      this.$bus.$on("updateGroupCreated", this.queryGroupCreated);
      this.queryGroupCreated();
    }
  };
  </script>
  
  <style>
  .container {
    width: 90%;
    margin: 0 auto;
  }
  
  .scroll-box {
    height: 300px;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow-x: hidden; /* 确保内容不溢出产生横向滚动条 */
  }
  
  .item {
    margin-bottom: 9px;
  }
  
  .el-card {
    border: none;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .card-content {
    padding: 1.5px;
  }
  
  .group-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .group-details {
    /* 让群组详情占据剩余空间 */
    flex: 1; 
  }
  
  .group-name {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 1px; /* 调整群组名称和描述的间距 */
  }
  
  .group-description {
    font-size: 16px;
    color: #555;
    margin-bottom: 0px; /* 调整群组描述和编辑按钮的间距 */
  }
  
  .edit-button-container {
    margin-left: auto; /* 将编辑按钮推到最右边 */
  }
  
  .el-button.edit-button {
    color: #409eff;
    padding: 0;
  }
  </style>
   -->