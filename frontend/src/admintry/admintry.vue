

<template>
    
    <div>
    <Header></Header>
    <el-input
        type="textarea"
        :rows="3"
        placeholder="请输入内容"
        v-model="inputTitle">
    </el-input>
    <el-input
        type="textarea"
        :rows="3"
        placeholder="请输入内容"
        v-model=" inputContant">
    </el-input>

    <button @click="test">点我测试发公告功能</button>
    </div>

    
</template>


<script>
import Header from '../components/Header.vue'
import axios from 'axios'

// const axiosInstance = axios.create({
//     baseURL:'http://127.0.0.1:8000',
//     headers:{
//     'Content-Type':'application/json'
//     }
// });

// axiosInstance.interceptors.request.use(
// config =>{const token= localstorage.getItem('token');
//     if(token){
//         config.headers['Authorization'] = `Bearer ${token}`;
//         return config;
//     },
// }
//     error => {
//         return Promise.reject(error);
//     }
// );

// export default axiosInstance;
export default {
    name:'Admintry',
    components: {
        Header,
    },
  data() {
    return {
      inputTitle: '',
      inputContant: '',
    }
  },
  methods: {
    
  }
}
</script>

<style scoped>
<style>