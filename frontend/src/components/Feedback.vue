<template>
    <v-container>
      <v-form v-model="valid" ref="form">
        <v-text-field
          v-model="name"
          :rules="[rules.required]"
          label="您的称呼*"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="email"
          :rules="[rules.required, rules.email]"
          label="您的邮箱地址*"
        ></v-text-field>
  
        <v-textarea
          v-model="advice"
          label="您对我们的产品有什么建议吗？(可选)"
        ></v-textarea>
  
        <v-textarea
          v-model="complaint"
          label="投诉(可选)"
        ></v-textarea>
  
        <span>
          请给我们的产品打分
        </span>
        <v-rating
          v-model="rating"
          background-color="yellow"
          color="yellow darken-3"
          large
        ></v-rating>
  
        <v-btn :disabled="!valid" @click="submit">
          Submit
        </v-btn>
      </v-form>
  
      <!-- 感谢图片对话框 -->
      <v-dialog v-model="showThankYouDialog" persistent max-width="400px">
        <v-card>
          <v-card-title class="headline">感谢您的反馈！</v-card-title>
          <v-card-text>
            <v-img
              src="../assets/thanks.png"
              alt="Thank you"
              max-width="100%"
            ></v-img>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="closeDialog">关闭</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        valid: false,
        name: '',
        email: '',
        advice: '',
        complaint: '',
        rating: null,
        showThankYouDialog: false, // 控制感谢图片对话框的显示
        rules: {
          required: value => !!value || 'Required.',
          email: value => {
            const pattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/
            return pattern.test(value) || 'Invalid e-mail.'
          }
        }
      }
    },
    methods: {
      submit() {
        if (this.$refs.form.validate()) {
          console.log(this.name, this.email, this.advice, this.complaint, this.rating)
          this.showThankYouDialog = true // 提交后显示感谢图片对话框
        }
      },
      closeDialog() {
        this.showThankYouDialog = false
      }
    }
  }
  </script>
  
  <style scoped>
  .v-container {
    max-width: 600px;
    margin: 0 auto;
  }
  </style>
  