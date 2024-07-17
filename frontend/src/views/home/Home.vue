<template>
    <div>
      <Header></Header>
      <h1>welcome,别急</h1>
      <News></News>
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
</style>