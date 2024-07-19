<template>
    <div class="container">
      <el-scrollbar class="scroll-box" wrap-style="overflow-x:hidden;">
        <el-card
          v-for="group in groupCreated"
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
                <el-button type="text" class="edit-button" @click="editGroup(group)">编辑</el-button>
              </div>
            </div>
            <el-dialog
              :visible.sync="editDialogVisible"
              title="修改群组信息"
              width="30%"
              :before-close="handleClose"
            >
              <el-form :model="editForm" label-position="top" ref="editForm">
                <el-form-item label="Group Name" prop="group_name">
                  <el-input v-model="editForm.group_name"></el-input>
                </el-form-item>
                <el-form-item label="Group description" prop="group_description">
                  <el-input v-model="editForm.description"></el-input>
                </el-form-item>
                <el-form-item label="Password" prop="password">
                  <el-input v-model="editForm.password"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveGroup">保存</el-button>
                  <el-button @click="editDialogVisible = false">取消</el-button>
                </el-form-item>
              </el-form>
            </el-dialog>
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
        editDialogVisible: false, // 控制编辑对话框的显示
        editForm: {
          group_name: "",
          description: "",
          password: ""
        },
        editingGroup: null // 保存当前编辑的组信息
      };
    },
    methods: {
      editGroup(group) {
        // 设置当前编辑的组信息
        this.editingGroup = group;
        // 将组信息填充到编辑表单中
        this.editForm.group_name = group.group_name;
        this.editForm.description = group.description;
      
        this.editForm.password = group.password;
        // 显示编辑对话框
        this.editDialogVisible = true;
      },
      saveGroup() {
        // 保存编辑后的数据
        if (this.editingGroup) {
          this.editingGroup.group_name = this.editForm.group_name;
          this.editingGroup.password = this.editForm.password;
          this.editingGroup.description = this.editForm.description;
        }
        // 关闭编辑对话框
        this.editDialogVisible = false;
      },
      handleClose(done) {
        this.editingGroup = null;
        done(); // 确认关闭对话框操作
      },
      queryGroupCreated() {
        // Your query logic here
      }
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
  