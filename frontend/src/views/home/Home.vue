<template>
    <div class="container">
      <Header></Header>
      <News class="news"></News>
      <h1 style="float: left;">TODO 能力形象化 + 前几次登录时间</h1>
    </div>
    
</template>
  
<script>
  import Header from '../../components/Header.vue'
  import News from './News.vue'

  export default {
    components: {
      Header,
      News
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
</style>