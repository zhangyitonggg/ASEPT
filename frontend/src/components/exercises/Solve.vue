<template>
  <v-container>
    <!-- 省略其他部分 -->
    <v-form @submit.prevent="submitForm" v-if="question">
      <v-card>
        <v-card-title>{{ question.title }}</v-card-title>
        <v-card-text>
          <p>{{ question.content }}</p>
          <template v-if="question.type === 'SINGLE_CHOICE' && question.choices">
            <v-radio-group v-model="answer">
              <v-radio
                v-for="(choice, key) in question.choices"
                :key="key"
                :label="`${key}. ${choice}`"
                :value="key"
              ></v-radio>
            </v-radio-group>
          </template>
          <template v-else-if="question.type === 'MULTI_CHOICE' && question.choices">
            <v-checkbox
              v-for="(choice, key) in question.choices"
              :key="key"
              :label="`${key}. ${choice}`"
              :value="key"
              v-model="selectedAnswers"
              @change="updateAnswers"
            ></v-checkbox>
          </template>
          <template v-else-if="question.type === 'BLANK_FILLING'">
            <v-text-field
              v-model="answer"
              label="填空"
            ></v-text-field>
          </template>
        </v-card-text>
      </v-card>
      <v-btn type="submit" color="primary">提交</v-btn>
    </v-form>
    <!-- 省略其他部分 -->
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
      selectedAnswers: [], // 多选题选项
      answer: '', // 单选题和填空题答案
      isSingleChoice: true,
      resultMessage: '',
      resultType: '',
      correctAnswers: null,
      showAnswers: false,
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
    updateAnswers() {
      this.answer = this.selectedAnswers;
    },
    formatAnswerForSubmission() {
      let formattedAnswer = {};
      if (this.question.type === 'SINGLE_CHOICE') {
        // 单选题
        formattedAnswer = { [this.answer]: this.question.choices[this.answer] };
      } else if (this.question.type === 'MULTI_CHOICE') {
        // 多选题
        formattedAnswer = this.selectedAnswers.reduce((acc, answer) => {
          acc[answer] = this.question.choices[answer];
          return acc;
        }, {});
      } else if (this.question.type === 'BLANK_FILLING') {
        // 填空题
        formattedAnswer = Array.isArray(this.answer) ? this.answer.reduce((acc, answer) => {
          acc[answer] = this.question.choices[answer];
          return acc;
        }, {}) : {};
      }
      return JSON.stringify(formattedAnswer);
    },
    submitForm() {
      const payload = {
        pid: this.pid,
        answer: this.formatAnswerForSubmission() // Convert answer to JSON string
      };
      this.$store
        .dispatch('submitAnswer', payload)
        .then(res => {
          if (res.is_correct) {
            this.resultMessage = '回答正确';
            this.resultType = 'success';
          } else {
            this.resultMessage = '回答错误';
            this.resultType = 'error';
          }
          this.showAnswers = false;
        })
        .catch(error => {
          this.$store.commit('setAlert', {
            type: 'error',
            message: error,
          });
        });
    },
    fetchCorrectAnswers() {
      this.$store
        .dispatch('getCorrectAnswersById', this.pid)
        .then(res => {
          this.correctAnswers = this.parseAnswers(res);
          this.showAnswers = true;
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

