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
                prepend-inner-icon="mdi-fingerprint"
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
                prepend-inner-icon="mdi-fingerprint"
                v-model="password"
                :disabled="loading"
              />
              <v-text-field
                class="dense"
                outlined
                label="确认密码"
                :rules="[v => v == password || '两次密码不一致']"
                type="password"
                prepend-inner-icon="mdi-fingerprint"
                required
                v-model="confirm_password"
                :disabled="loading"
              />
              <v-btn
                block
                depressed
                color="primary"
                type="submit"
                :disabled="loading"
              > 修改 </v-btn>
            </v-form>
            <v-btn
              block
              depressed
              @click.stop="switchRegisterPage"
              :disabled="loading"
              class="mt-2"
              color="error"
            > 注销 </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-card>
      <v-card-title>
        <h2 class="mb-10">
          查看您的状态
        </h2>
      </v-card-title>
      <v-card-text>
        <v-row class="pl-3 pr-3">
          <v-col>
            <user_status :passedQuestions="passedQuestions" :failedQuestions="failedQuestions"></user_status>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import user_status from '@/components/UserStatusChart.vue';

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
      this.loading = true;
      this.$store.dispatch('userModify', this.user).then(() => {
        this.loading = false;
      });
    }
  },
  components: {
    user_status
  }
}
</script>