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
        <v-alert v-if="resultMessage" :type="resultType" class="mt-4">
          {{ resultMessage }}
        </v-alert>
        <v-btn v-if="resultMessage && !showAnswers" @click="fetchCorrectAnswers" color="secondary" class="mt-4">
          显示答案
        </v-btn>
        <v-card v-if="correctAnswers && showAnswers" class="mt-4">
          <v-card-title>正确答案</v-card-title>
          <v-card-text>
            <div v-if="question.type === 'SINGLE_CHOICE'">
              <p>正确选项:</p>
              <ul>
                <li v-for="(value, key) in correctAnswers" :key="key">{{ `${key}. ${value}` }}</li>
              </ul>
            </div>
            <div v-else-if="question.type === 'MULTI_CHOICE'">
              <p>正确选项:</p>
              <ul>
                <li v-for="(value, key) in correctAnswers" :key="key">{{ `${key}. ${value}` }}</li>
              </ul>
            </div>
            <div v-else-if="question.type === 'BLANK_FILLING'">
              <p>正确答案:</p>
              <ul>
                <li v-for="(answer, index) in correctAnswers" :key="index">{{ `${index}: ${answer}` }}</li>
              </ul>
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
      selectedAnswers: [], // 用于多选题选项
      answer: '', // 用于单选题和填空题答案
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
        const answers = this.answer.split(' ').filter(a => a.trim() !== '');
        formattedAnswer = answers.reduce((acc, answer, index) => {
          acc[index + 1] = answer;
          return acc;
        }, {});
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

<style>
.fixed-button {
  position: fixed;
  left: 3%;
  top: 15%;
  z-index: 5;
}
</style>
