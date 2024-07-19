<template>
  <div class="container">
    <el-collapse v-model="activeName" accordion class="custom-collapse">
      <el-collapse-item
        v-for="group in groupAdded"
        :key="group.gid"
        :title="group.group_name"
        :name="group.gid"
        class="custom-collapse-item"
      >
        <div class="description">{{ group.description }}</div>
        <div class="password">密码: {{ group.password }}</div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        activeName: '0',
        groupAdded: [
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
        ]
      };
    }
  }
</script>

<style>
  .container {
    width: 90%;
    margin: 0 auto;
  }
  
  .custom-collapse {
    height: 300px;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    overflow-y: auto; /* 添加垂直滚动条 */
    overflow-x: hidden; /* 确保内容不溢出产生横向滚动条 */
    background: linear-gradient(135deg, #f3f4f7, #fff);
  }

  .custom-collapse-item {
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 10px;
    background: #fff;
    transition: transform 0.3s, box-shadow 0.3s;
  }

  .custom-collapse-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  .custom-collapse-item .el-collapse-item__header {
    background: linear-gradient(135deg, #42b983, #2c8e7d);
    color: #fff;
    border-radius: 8px 8px 0 0;
    padding: 10px;
  }

  .custom-collapse-item .el-collapse-item__header:hover {
    background: linear-gradient(135deg, #2c8e7d, #42b983);
  }

  .custom-collapse-item .el-collapse-item__wrap {
    border-radius: 0 0 8px 8px;
    padding: 10px;
    background: #fafafa;
  }

  .description {
    margin-bottom: 5px;
  }

  .password {
    font-weight: bold;
    color: #ff6f61;
  }
</style>
