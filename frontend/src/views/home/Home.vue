<template>
    <div class="container">
      <Header></Header>
      <a class="test" href="/admintry">点我测试管理员功能</a>
      <News class="news"></News>
    </div>
  </template>
  
  <script>
  import Header from '../../components/Header.vue'
  import News from './News.vue'
  import Mine from '../../mine/Mine.vue'
  import Admintry from '../../admintry/admintry.vue'

  export default {
    components: {
      Header,
      News,
      Mine,//here
      Admintry,
    }
  };
  </script>
  
  <style scoped>
  .container {
    position: relative;
    width: 100%;
    height: 100vh; /* 你可以根据需要调整高度 */
  }
  
  .news {
    position: absolute;
    right: 5%;
    top: 15%; /* 你可以根据需要调整top值 */
  }

  .Mine {
    margin-top:50px;
  }

  .test {
    margin-top: 20px;
  }
  </style>