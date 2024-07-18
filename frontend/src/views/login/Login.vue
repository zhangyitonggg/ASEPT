<template>
    <div>
      <el-card class="box-card">
        <h2>登录SEP</h2>

        <el-form
          :model="ruleForm"
          status-icon
          :rules="rules"
          ref="ruleForm"
          label-position="left"
          label-width="70px"
          class="login-from"
        >

          <el-form-item label="用户名" prop="uname">
            <el-input v-model="ruleForm.uname"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              type="password"
              v-model="ruleForm.password"
              autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-form>
        
        <div class="btnGroup">
          <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
          <router-link to="/register">
            <el-button style="margin-left:10px">注册</el-button>
          </router-link>
        </div>
      
        </el-card>
    </div>
  </template>
  
  <script>
  import qs from 'qs'
  import axios from 'axios'
  import { setToken } from '@/utils/auth'
  
  export default {
    data() {
      return {
        ruleForm: {
          uname: "",
          password: "",
        },
        rules: {
          uname: [
            { required: true, message: "用户名不能为空！", trigger: "blur" },
          ],
          password: [
            { required: true, message: "密码不能为空！", trigger: "blur" },
          ],
        },
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => { // 根据上面的rules进行检验合法性
          this.$store.dispatch('storeUname', this.ruleForm.uname)
          if (valid) {
            // http://localhost:8080/login/security/token
            axios({
              url:'http://localhost:8080/login/security/token',
              method:'post',
              data: qs.stringify({
                username: this.ruleForm.uname,
                password: this.ruleForm.password
              }),
            })
            .then(
              response => {
                // response.setHeader("Access-Control-Allow-Origin",'*')
                alert("submit!");
                const token  = response.data;
                setToken(token);
                console.log('token:',token);
                this.$router.push({ path: '/home' });
              },
              error => {
                alert("登录失败，请检查用户名和密码");
                return false;
              }
            )
          } else {
            console.log("error submit!!");
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
    },
  };
  </script>
  
  <style scoped>
  .box-card {
    position: absolute;
    left: 50%;
    top:40%;
    transform: translate(-50%,-50%);

    margin: auto auto;
    width: 400px;
  }
  .login-from {
    margin: auto auto;
  }
  </style>