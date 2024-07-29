<template>
  <v-container>
    <v-form v-model="valid" ref="form">
      <v-text-field v-model="name" :rules="[rules.required]" label="您的称呼*" required></v-text-field>
      <v-text-field v-model="email" :rules="[rules.required, rules.email]" label="您的邮箱地址*"></v-text-field>
      <v-textarea v-model="advice" label="您的建议(可选)"></v-textarea>
      <v-textarea v-model="complaint" label="投诉(可选)"></v-textarea>
      <v-btn :disabled="!valid" @click="submit" color="primary" :loading="loading">
        提交
      </v-btn>
    </v-form>
    <v-dialog v-model="showThankYouDialog" persistent max-width="400px">
      <v-card>
        <v-card-title class="headline">感谢您的反馈！</v-card-title>
        <v-card-text>
          <v-img src="../assets/thanks.png" alt="Thank you" max-width="100%"></v-img>
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
      loading: false,
      valid: false,
      name: '',
      email: '',
      advice: '',
      complaint: '',
      showThankYouDialog: false,
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
        this.loading = true;
        this.$store.dispatch('submitFeedback', {
          name: this.name,
          email: this.email,
          advice: this.advice,
          complaint: this.complaint,
        })
        .then((res) => {
          this.showThankYouDialog = true;
        })
        .catch((e) => {
          this.$store.commit('setAlert', {
            message: e,
            type: 'error'
          });
        })
        .finally(() => {
          this.loading = false;
        });
      }
    },
    closeDialog() {
      this.showThankYouDialog = false;
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