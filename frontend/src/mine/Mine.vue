<template>
    <div>
      <Header></Header>
      <div class="mine-start">
        <Avatar></Avatar>
        <div class="mine-contains">
          <div class="name">hh: {{$store.state.uname}}</div><br/>

            <el-descriptions class="margin-top"  :column="1"> 
              <el-descriptions-item label="用户等级">
                <el-tag>{{$store.state.ulevel}}级</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="上传题目数">
                <el-tag>{{$store.state.uquestionNum}}道</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </div>
          
        
      </div>
      
    
      <el-row :gutter="20">
        <el-button type="danger" class="danger-button" round>修改头像</el-button>
        <el-button type="danger" class="danger-button" round>修改密码</el-button>
        <el-button type="danger" class="danger-button" round>退出登录</el-button>
        </el-row>
    </div>
</template>



<script>
import Avatar from './Avatar.vue'
import Header from '../components/Header.vue'

    export default {
        name:'Mine',
        components: {
            Header,
            Avatar,
        }
    };

</script>




<style scoped>

    .danger-button {
      width: 200px;
      padding: 30px;
    }

    .name {
      font-size:50px;
      font-weight:bold;
      text-align:left;
    }

    .mine-start {
      display: flex;
      align-items: left;
      margin-left:200px;
      margin-bottom: 30px;
      margin-top: 30px;
    }

    .mine-contains {
      margin-left:50px;
    }

   
</style>