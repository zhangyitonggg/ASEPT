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
    <v-card>
      <v-card-title>
        <h2 class="mb-10">
          查看您的状态
        </h2>
      </v-card-title>
      <v-container fluid class="d-flex justify-center align-center" v-if="status_loading">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </v-container>
      <v-card-text v-else>
        <v-row class="pl-3 pr-3">
          <v-col>
            <time_status
              :lastUpdateTime="new Date().toLocaleString()"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col v-if="choicePassedQuestions+choiceFailedQuestions != 0">
            <user_status
              :data="[choicePassedQuestions, choiceFailedQuestions]"
              :labels="['通过次数', '错误次数']"
              :backgroundColor="['#4FCF95FF', '#D30B0BFF']"
              :title="'选择题统计'"
            ></user_status>
          </v-col>
          <v-col v-if="choicePassedQuestions+blankPassedQuestions+choiceFailedQuestions+blankFailedQuestions != 0">
            <user_status
              :data="[choicePassedQuestions, blankPassedQuestions, choiceFailedQuestions, blankFailedQuestions]"
              :labels="['选择通过次数', '填空通过次数', '选择错误次数', '填空错误次数']"
              :backgroundColor="['#4FCF95FF', '#4FCF95FF', '#D30B0BFF', '#D30B0BFF']"
              :title="'总计'"
            ></user_status>
          </v-col>
          <template v-else>
            <v-col>
              <v-banner
                outlined
                type="info"
                icon="mdi-gauge-empty"
              >
                <h2>
                  您还没有做过题目。去做点题吧。
                </h2>
              </v-banner>
            </v-col>
          </template>
          <v-col v-if="blankPassedQuestions+blankFailedQuestions != 0">
            <user_status
              :data="[blankPassedQuestions, blankFailedQuestions]"
              :labels="['通过次数', '错误次数']"
              :backgroundColor="['#4FCF95FF', '#D30B0BFF']"
              :title="'填空题统计'"
            ></user_status>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import user_status from '@/components/UserStatusChart.vue';
import time_status from '@/components/UserStatusChartByTime.vue';

export default {
  name: 'MyInfo',
  data() {
    return {
      loading: false,
      status_loading: true,
      original_password: null,
      password: null,
      confirm_password: null,
      choicePassedQuestions: 0,
      choiceFailedQuestions: 0,
      blankPassedQuestions: 0,
      blankFailedQuestions: 0,
    }
  },
  mounted() {
    this.$store.commit('setAppTitle', "个人信息");
    this.$store.dispatch('getUserStatus')
      .then((res) => {
        this.choicePassedQuestions = res.choice_correct;
        this.choiceFailedQuestions = res.choice_submit - res.choice_correct;
        this.blankPassedQuestions = res.blank_correct;
        this.blankFailedQuestions = res.blank_submit - res.blank_correct;
      })
      .catch((e) => {
        this.$store.commit('setAlert', { message: e, type: 'error' });
      })
      .finally(() => {
        this.status_loading = false;
      });
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
  components: {
    user_status,
    time_status,
  }
}
</script>