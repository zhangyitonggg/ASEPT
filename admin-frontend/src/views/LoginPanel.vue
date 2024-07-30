<template>
  <v-card flat>
    <v-progress-linear :indeterminate="true" v-show="loading" id="loginPanelProgressBar" color="success" />
    <div class="ma-6">
      <h2 class="mb-4">
        欢迎回来，管理员。
      </h2>
      <v-subheader id="loginPanelSubheader">
        <template v-if="loading">
          <span v-if="showRegister">正在联系远程服务器</span>
          <span v-else>正在验证你的身份</span>
        </template>
        <span v-else>
          <span>要继续访问，请使用你的账号登录。</span>
        </span>
      </v-subheader>
      <v-form class="loginPanelForm" @submit.prevent="handleLogin">
        <v-text-field class="dense" outlined label="用户名" type="text" prepend-inner-icon="mdi-account-box"
          :rules="[v => !!v || '']" v-model="username" required :disabled="loading" />
        <v-text-field class="dense" outlined label="密码" type="password" prepend-inner-icon="mdi-fingerprint"
          :rules="[v => !!v || '']" required v-model="password" :disabled="loading" />
        <div class="d-flex">
          <v-checkbox class="dense" v-model="remember" label="在这台设备上记住我" color="primary"
            @change="warnAboutRememberingLogin" :disabled="loading" />
          <v-spacer />
        </div>
        <v-btn depressed block color="primary" type="submit" :disabled="loading">
          登录
        </v-btn>
      </v-form>
    </div>
  </v-card>
</template>

<script>
import { vuetify } from 'vuetify';

export default {
  name: "LoginPanel",
  data() {
    return {
      username: "",
      password: "",
      remember: false,
      showRegister: false,
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      try {
        await this.$store.dispatch("login", {
          username: this.username,
          password: this.password,
          remember: this.remember,
        });
        this.$store.commit("getUserName");
        this.$store.commit('setAlert', {
          type: "success",
          message: "欢迎回来，" + this.$store.getters.username + "。",
        });
        this.$router.push("/");
      } catch (error) {
        this.$store.commit("setAlert", {
          type: "error",
          message: error,
        });
      } finally {
        this.loading = false;
      }
    },
    warnAboutRememberingLogin() {
      if (this.remember) {
        this.$store.commit("setAlert", {
          type: "warning",
          message: "我们不建议管理员勾选此选项。",
        });
      }
    },
  },
};
</script>

<style scoped lang="scss">
.dense {
  margin: -5px 0 -10px 0 !important;
}

.topmost {
  z-index: 1001;
}

.v-card {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

#loginPanelProgressBar {
  position: absolute;
  top: -30px;
  margin: 0 0 0 0;
}

.loginPanelForm {
  width: 100%;
  z-index: 2;
  position: relative;
}

#loginPanelSubheader {
  clear: both;
  padding-bottom: 20px;
  padding-left: 0;
}
</style>
