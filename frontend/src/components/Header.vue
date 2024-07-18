<template>
  <!-- 能力形象化 + 新闻 + 前几次登录时间？ -->
  <!-- 刷题，可以根据难度、题目类型、科目等；训练时可以将题目加入某个问题组；举报题目；全局搜索题目？ -->
  <!-- 对自己的所有问题组进行管理（包括新建加删除加移除其中的某个题目）；上传题目；将某个问题组分享给某个已加入的用户组-->
  <!-- 搜索公开的用户组；创建用户组（可以设置为任何人可以加入或者通过密码假如；加入用户组；退出用户组）-->
  <!-- 退出账号；修改密码：修改头像；上传题目数目；等级（通过上传题目数目+正确率+答题数确定？）--> 
  <div class="header">
    <div class="img">
      <img src="../assets/logo.png" alt="">
    </div>
    <el-menu
      :default-active="this.$route.path"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      router
      background-color="#fff"
      text-color="#333"
      active-text-color="#0084ff"
      style="flex:1"
    >
      <el-menu-item v-for="(item, i) in navList" :key="i" :index="item.name">
        <template slot="title">
          <span> {{ item.navItem }}</span>
        </template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
    data() {
    return {
        navList:[
            {name:'/home', navItem:'首页'},
            {name:'/exercise',navItem:'训练'},
            {name:'/resources',navItem:'资源'},
            {name:'/groups',navItem:'群组'},
            {name:'/mine',navItem:'个人中心'},
        ]                      
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      }
  }
}
</script>

<style>
.el-menu-item{
  font-size: 18px !important;
}
.el-menu-item.is-active {
    color: #ea5b2c !important;
    font-size: 18px !important;
}
.el-menu--horizontal>.el-menu-item.is-active {
  border-bottom: 2px solid #ea5b2c !important;
}
</style>
<style scoped>
.header {
  display: flex;
  width: 100%;
  .img {
    background: #ffffff;
    border-bottom: solid 1px #e6e6e6;
    img {
      height:50px;
      padding:10px;
    }
  }
}
</style>






