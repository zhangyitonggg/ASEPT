<template>
  <v-container>
    <v-card class="mb-10">
      <v-card-title>
        <h2 class="mb-10">
          管理您的账号
        </h2>
      </v-card-title>
      <v-card-text>
        <v-row class="mb-5 pl-7">
          <v-avatar
            color="primary"
            size="128"
          ><img src="https://cravatar.cn/avatar/5ed20f2960c5e87468dee55bfd3ec4ab?d=mp">
          </v-avatar>
        </v-row>
        <v-row class="pl-3 pr-3">
          <v-col>
            <v-form @submit.prevent="handleUserModify">
              <v-text-field
                class="dense"
                outlined
                label="用户名"
                autofocus
                prepend-inner-icon="mdi-account-box"
                v-model="$store.getters.username"
                disabled
              />
              <v-text-field
                class="dense"
                outlined
                label="原密码"
                type="password"
                prepend-inner-icon="mdi-fingerprint-off"
                required
                v-model="original_password"
                :disabled="loading"
              />
              <v-text-field
                class="dense"
                outlined
                label="新密码"
                :rules="[
                  v => !v || v.length > 8 || '至少9字符',
                  v => !v || v.length < 21 || '至多20字符',
                  v => {
                      if (!v) return true;
                      const pattern = /^.*[0-9].*$/;
                      const pattern_w = /^.*[a-zA-Z].*$/;
                      return (pattern.test(v) && pattern_w.test(v)) || '必须包含数字和字母';
                    }
                ]"
                type="password"
                prepend-inner-icon="mdi-account-key"
                v-model="password"
                :disabled="loading"
              />
              <v-text-field
                class="dense"
                outlined
                label="确认密码"
                :rules="[v => v == password || '两次密码不一致']"
                type="password"
                prepend-inner-icon="mdi-account-key-outline"
                required
                v-model="confirm_password"
                :disabled="loading"
              />
              <v-btn
                block
                depressed
                color="primary"
                type="submit"
                @click.stop="handleUserModify"
                :disabled="loading"
                :loading="loading"
              > 修改 </v-btn>
            </v-form>
            <v-btn
              block
              depressed
              @click.stop="logout"
              :disabled="loading"
              class="mt-2"
              color="error"
            > 注销 </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'MyInfo',
  data() {
    return {
      loading: false,
      original_password: null,
      password: null,
      confirm_password: null,
      passedQuestions: 20,
      failedQuestions: 5
    }
  },
  mounted() {
    this.$store.commit('setAppTitle', "个人信息");
  },
  methods: {
    handleUserModify() {
      if (this.password !== this.confirm_password) {
        this.$store.commit('setAlert', { message: '两次密码不一致', type: 'error' });
        return;
      } else if (this.password === this.original_password) {
        this.$store.commit('setAlert', { message: '新密码不能与原密码相同', type: 'error' });
        return;
      } else if (this.password.length < 9 || this.password.length > 20) {
        this.$store.commit('setAlert', { message: '密码长度应在 9 - 20 字符之间', type: 'error' });
        return;
      }
      this.loading = true;
      this.$store.dispatch('userModify', {username: this.$store.getters.username, originalPassword: this.original_password, newPassword: this.password})
        .then(() => {
          this.$store.commit('setAlert', { message: '用户信息修改成功。', type: 'success' });
        })
        .catch((e) => {
          this.$store.commit('setAlert', { message: e, type: 'error' });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    logout() {
      this.$store.commit("clearPersonalInfo");
      this.$router.push({ name: 'login' });
    }
  },
}
</script>