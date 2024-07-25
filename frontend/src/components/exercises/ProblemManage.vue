<template>
  <v-container>
    <v-btn
      class="fixed-button"
      fab
      dark
      color="indigo"
      @click="returnback"
    >
      <v-icon dark>
        mdi-arrow-u-left-bottom-bold
      </v-icon>
    </v-btn>

    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-form @submit.prevent="submitForm" v-if="question">
          <v-card>
            <v-card-title>{{ question.title }}</v-card-title>
            <v-card-text>
              <p>{{ question.content }}</p>
              <template v-if="question.type === 'SINGLE_CHOICE' && question.choices">
                <template v-if="isSingleChoice">
                  <v-radio-group v-model="answer">
                    <v-radio
                      v-for="(choice, key) in question.choices"
                      :key="key"
                      :label="`${key}. ${choice}`"
                      :value="key"
                    ></v-radio>
                  </v-radio-group>
                </template>
                <template v-else>
                  <v-checkbox-group v-model="answer">
                    <v-checkbox
                      v-for="(choice, key) in question.choices"
                      :key="key"
                      :label="`${key}. ${choice}`"
                      :value="key"
                    ></v-checkbox>
                  </v-checkbox-group>
                </template>
              </template>
              <template v-else-if="question.type === 'FILL_BLANK'">
                <v-text-field
                  v-for="(blank, index) in question.answers"
                  :key="index"
                  v-model="answer[index]"
                  :label="`Blank ${index + 1}`"
                ></v-text-field>
              </template>
            </v-card-text>
          </v-card>
          <v-btn type="submit" color="primary">Submit</v-btn>
        </v-form>
        <v-alert v-if="resultMessage" type="success" class="mt-4">
          {{ resultMessage }}
        </v-alert>
        <v-alert v-if="errorMessage" type="error" class="mt-4">
          {{ errorMessage }}
        </v-alert>
        <v-card v-if="correctAnswers" class="mt-4">
          <v-card-title>Correct Answers</v-card-title>
          <v-card-text>
            <v-btn @click="showAnswers" color="primary">Show Answers</v-btn>
            <div v-if="showingAnswers">
              <div v-if="question.type === 'SINGLE_CHOICE'">
                <p>Correct Choice(s):</p>
                <ul>
                  <li v-for="(value, key) in correctAnswers" :key="key">{{ `${key}. ${value}` }}</li>
                </ul>
              </div>
              <div v-else-if="question.type === 'FILL_BLANK'">
                <p>Correct Answers:</p>
                <ul>
                  <li v-for="(answer, index) in correctAnswers" :key="index">{{ `Blank ${index + 1}: ${answer}` }}</li>
                </ul>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    pid: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      question: null,
      answer: {},
      isSingleChoice: true,
      resultMessage: '',
      errorMessage: '',
      correctAnswers: null,
      showingAnswers: false,
    };
  },
  created() {
    this.fetchQuestion();
  },
  methods: {
    fetchQuestion() {
      this.$store
        .dispatch('getProblemById', this.pid)
        .then(res => {
          this.question = {
            pid: res.pid,
            title: res.title,
            content: res.content,
            type: res.type,
            author: res.author,
            update_time: res.update_time,
            is_public: res.is_public,
            choices: this.parseChoices(res.choices),
            answers: [] // 初始时不包含答案
          };
          console.log(this.question);
          this.isSingleChoice = this.question.answers && Object.keys(this.question.answers).length === 1;
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    parseChoices(choices) {
      if (choices) {
        return JSON.parse(choices);
      }
      return null;
    },
    parseAnswers(answers) {
      if (answers) {
        return JSON.parse(answers);
      }
      return [];
    },
    submitForm() {
      // 将答案转换为 JSON 格式的字符串
      const formattedAnswer = this.formatAnswerForSubmission();

      this.$store
        .dispatch('submitAnswer', { pid: this.pid, answer: formattedAnswer })
        .then(res => {
          if (res.status === 'success') {
            this.resultMessage = res.is_correct ? '回答正确' : '回答错误';
            this.errorMessage = '';
          } else {
            this.resultMessage = '';
            this.errorMessage = '提交失败';
          }
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    formatAnswerForSubmission() {
      let formattedAnswer = {};
      if (this.question.type === 'SINGLE_CHOICE' || this.question.type === 'MULTI_CHOICE') {
        if (Array.isArray(this.answer)) {
          // 多选题的答案处理
          formattedAnswer = this.answer.reduce((acc, choice) => {
            acc[choice] = this.question.choices[choice];
            return acc;
          }, {});
        } else {
          // 单选题的答案处理
          formattedAnswer[this.answer] = this.question.choices[this.answer];
        }
      } else if (this.question.type === 'FILL_BLANK') {
        // 填空题的答案处理
        formattedAnswer = this.answer;
      }
      return JSON.stringify(formattedAnswer);
    },
    showAnswers() {
      this.$store
        .dispatch('getProblemAns', this.pid)
        .then(res => {
          this.correctAnswers = this.parseAnswers(res.data);
          this.showingAnswers = true;
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    returnback() {
      this.$router.go(-1);
    },
  },
};
</script>

<style>
.fixed-button {
  position: fixed;
  left: 3%;
  top: 15%;
  z-index: 5;
}
</style>
