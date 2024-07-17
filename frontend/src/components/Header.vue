<template>
    <nav class="header">
      <div class="header-menu">
        <div class="header-start">
          <div class="header-logo-text">SEP</div>
          <a class="header-item-first" href="/home">首页</a> <!-- 能力形象化 + 新闻 + 前几次登录时间？ -->
          <a class="header-item" href="/exercise">训练</a>  <!-- 刷题，可以根据难度、题目类型、科目等；训练时可以将题目加入某个问题组；举报题目；全局搜索题目？ -->
          <a class="header-item" href="/resources">资源</a> <!-- 对自己的所有问题组进行管理（包括新建加删除加移除其中的某个题目）；上传题目；将某个问题组分享给某个已加入的用户组-->
          <a class="header-item" href="/group">群组</a> <!-- 搜索公开的用户组；创建用户组（可以设置为任何人可以加入或者通过密码假如；加入用户组；退出用户组）-->
          <a class="header-item" href="/mine">个人中心</a> <!-- 退出账号；修改密码：修改头像；上传题目数目；等级（通过上传题目数目+正确率+答题数确定？）--> 
          <h1 class="mortor">welcome,{{$store.state.uname}}</h1>
        </div>
      </div>
    </nav>
</template>
  
<script>
    export default {
        name: 'Header',
    };
</script>

<style scoped>
    .mortor {
        font-size: 2rem;
        color: #eee;
        margin-left: 20rem;
    }
    .header {
        background-color: #333;
        color: #fff;
        padding: 1rem;
    }
    .header-logo-text {
        font-size: 3rem;
        color:#fff;
        font-family: 'Arial', sans-serif;
    }
    .header-item-first {
        font-size: 2rem;
        color: #fff;
        margin-left: 10rem;
    }
    .header-item {
        font-size: 2rem;
        color: #fff;
        margin-left: 5rem;
    }
    .header-menu {
        display: flex;
        align-items: center;
    }
    .header-start {
        display: flex;
        align-items: center;
    }
    .header-item:hover {
        text-decoration: underline;
    }
</style>
  