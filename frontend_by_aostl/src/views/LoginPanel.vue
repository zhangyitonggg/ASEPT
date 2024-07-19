<template>
  <v-card flat>
    <v-progress-linear
      :indeterminate="true"
      v-show="loading"
      id="loginPanelProgressBar"
      color="success"
    />
    <div class="ma-6">
      <h2 class="mb-4">
          欢迎<span v-if="showRegister">新朋友！</span><span v-else>回来。</span>
      </h2>
      <v-subheader id="loginPanelSubheader">
          <template v-if="loading">
          <span v-if="showRegister">正在联系远程服务器</span>
          <span v-else>正在验证你的身份</span>
          </template>
          <span v-else>
          <span v-if="showRegister">
              填写下列信息，获得属于您的账号。
          </span>
          <span v-else>要继续访问，请使用你的账号登录。</span>
          </span>
      </v-subheader>
      <v-form
          v-if="showRegister"
          class="loginPanelForm"
          @submit.prevent="handleRegister"
      >
          <v-text-field
          class="dense"
          outlined
          label="用户名"
          :rules="[v => !!v || '必填']"
          autofocus
          required
          prepend-inner-icon="mdi-account-box"
          v-model="username"
          :disabled="loading"
          />
          <v-text-field
          class="dense"
          outlined
          label="密码"
          :rules="[
              v => !!v || '',
              v => v.length > 8 || '至少9字符',
              v => v.length < 21 || '至多20字符',
              v => {
              const pattern = /^.*[0-9].*$/
              const pattern_w = /^.*[a-zA-Z].*$/
              return (
                  (pattern.test(v) && pattern_w.test(v)) || '必须包含数字和字母'
              )
              }
          ]"
          type="password"
          prepend-inner-icon="mdi-fingerprint"
          required
          v-model="password"
          :disabled="loading"
          />
          <v-btn
          block
          depressed
          color="primary"
          type="submit"
          :disabled="loading"
          >
          注册
          </v-btn>
      </v-form>
      <v-form v-else class="loginPanelForm" @submit.prevent="handleLogin">
          <v-text-field
          class="dense"
          outlined
          label="用户名"
          type="text"
          prepend-inner-icon="mdi-account-box"
          :rules="[v => !!v || '']"
          v-model="username"
          required
          :disabled="loading"
          />
          <v-text-field
          class="dense"
          outlined
          label="密码"
          type="password"
          prepend-inner-icon="mdi-fingerprint"
          :rules="[v => !!v || '']"
          required
          v-model="password"
          :disabled="loading"
          />
          <div class="d-flex">
          <v-checkbox
              class="dense"
              v-model="remember"
              label="在这台设备上记住我"
              color="primary"
              @change="warnAboutRememberingLogin"
              :disabled="loading"
          />
          <v-spacer />
          </div>
          <v-btn
          depressed
          block
          color="primary"
          type="submit"
          :disabled="loading"
          >
          登录
          </v-btn>
      </v-form>
      <v-btn
          block
          depressed
          @click.stop="switchRegisterPage"
          :disabled="loading"
          class="mt-2"
      >
          {{ this.showRegister ? '已有账号？登录' : '没有账号？注册' }}
      </v-btn>
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
            message: "登录失败，请检查输入。",
          });
        } finally {
          this.loading = false;
        }
    },
    handleRegister() {
      this.loading = true;
      this.$store
        .dispatch("register", {
          username: this.username,
          password: this.password,
        })
        .then(() => {
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
          vuetify.framework.dialog.alert("注册失败，请检查输入。");
        });
    },
    switchRegisterPage() {
      this.showRegister = !this.showRegister;
    },
    warnAboutRememberingLogin() {
      if (this.remember) {
        this.$store.commit("setAlert", {
          type: "warning",
          message: "请不要在公共设备上勾选此选项。",
        });
      }
    },
  },
  beforeMount() {
    this.$store.commit("checkToken");
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

#loginPanelProgressBar {
  position: absolute;
  top: -30px;
  margin: 0 0 0 0;
}

.loginPanelForm {
  width: 100%;
}

#loginPanelSubheader {
  clear: both;
  padding-bottom: 20px;
  padding-left: 0;
}
</style>
