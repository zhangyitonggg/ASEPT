<template>
    <v-container fluid fill-height>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="10" md="8" lg="6">
          <!-- 聊天框 -->
          <v-card class="chat-container" outlined>
            <v-card-title>您的AI助手</v-card-title>
            <v-card-text class="chat-box">
              <!-- 消息列表 -->
              <v-container class="message-list">
                <v-row>
                  <v-col v-for="(message, index) in messages" :key="index" cols="12">
                    <v-card>
                      <v-card-text>{{ message }}</v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

          </v-card>
          <v-card class="chat-container2" outlined>
            <!-- 固定的输入框 -->
            <div class="fixed-input-row">
            <v-row no-gutters>
                <v-col cols="9">
                <v-text-field
                    v-model="inputMessage"
                    label="请输入消息"
                    outlined
                    dense
                    hide-details
                    @keyup.enter="sendMessage"
                ></v-text-field>
                </v-col>
                <v-col cols="3">
                <v-btn color="primary" @click="sendMessage" class="send-button">发送</v-btn>
                </v-col>
            </v-row>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    data() {
      return {
        inputMessage: '', // 用户输入的消息
        messages: [], // 消息列表
      }
    },
    mounted() {
      this.$store.commit('setAppTitle', 'AI助手');
      this.sendToApi("你好。")
    },
    methods: {
      // 发送消息
      sendMessage() {
        if (this.inputMessage !== '') {
          this.messages.push('用户：' + this.inputMessage) // 添加用户发送的消息到消息列表
          this.sendToApi(this.inputMessage) // 调用API接口获取回复
          this.inputMessage = '' // 清空输入框
        }
      },
      // 调用API接口
      async sendToApi(userMessage) {
        try {
          const response = await axios.post('https://aihubmix.com/v1/chat/completions', {
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: userMessage }]
          }, {
            headers: {
              'Authorization': 'Bearer sk-du8ZeyDgmoxJVg24771dFfFf646445A289018dAaBeD4A2Fa',
              'Content-Type': 'application/json'
            }
          })
          const aiReply = response.data.choices[0].message.content
          this.messages.push('AI：' + aiReply) // 将AI回复的消息添加到消息列表
        } catch (error) {
          console.error('Error:', error)
          this.messages.push('AI：抱歉，获取回复失败。') // 添加错误消息到消息列表
        }
      }
    }
  }
  </script>
  
  <style>
  .chat-container {
    position: relative; /* 为了使固定元素相对于chat-container定位 */
    display: flex;
    flex-direction: column;
    height: 80vh;
    max-height: 600px; /* 控制最大高度 */
    width: 100%; /* 使宽度适应容器 */
  }
  .chat-container2 {
    position: relative; /* 为了使固定元素相对于chat-container定位 */
    display: flex;
    margin-top: 4px;
    flex-direction: column;
    height: 60vh;
    max-height:70px; /* 控制最大高度 */
    width: 100%; /* 使宽度适应容器 */
  }
  
  .chat-box {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding-bottom: 56px; /* 留出输入框和按钮的高度 */
  }
  
  .message-list {
    overflow-y: auto;
    flex-grow: 1; /* 使消息列表填满剩余空间 */
  }
  
  .fixed-input-row {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 10px 0; /* 上下内边距 */
    display: flex;
    align-items: center;
    padding-left: 10px;
    padding-right: 10px;
  }
  
  .fixed-input-row .v-text-field {
    margin-right: 8px;
  }
  
  .fixed-input-row .send-button {
    margin-left: 20px;
    width: 110px; /* 设置按钮宽度 */
    flex-shrink: 0; /* 防止按钮被压缩 */
  }
  
  </style>
  