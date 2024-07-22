<template>
    <v-container>
      <v-form v-model="valid" ref="form">
        <v-text-field
          v-model="name"
          :rules="[rules.required]"
          label="Name"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="email"
          :rules="[rules.required, rules.email]"
          label="Email"
          required
        ></v-text-field>
  
        <v-textarea
          v-model="message"
          :rules="[rules.required]"
          label="Message"
          required
        ></v-textarea>
  
        <v-btn :disabled="!valid" @click="submit">
          Submit
        </v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        valid: false,
        name: '',
        email: '',
        message: '',
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
          // 假设 sendFeedback 是一个发送邮件的函数
          sendFeedback(this.name, this.email, this.message)
            .then(() => {
              this.$emit('success', 'Your feedback has been sent!')
            })
            .catch(err => {
              this.$emit('error', 'Failed to send feedback.')
              console.error(err)
            })
        }
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
  