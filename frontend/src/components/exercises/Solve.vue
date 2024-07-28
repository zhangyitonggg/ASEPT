<template>
  <div>
    <v-container fluid class="d-flex justify-center align-center" v-if="loading">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-container>
    <v-container v-else>
      <v-btn class="fixed-button" fab dark color="indigo" @click="returnback">
        <v-icon dark>
          mdi-arrow-u-left-bottom-bold
        </v-icon>
      </v-btn>

      <v-row justify="center">
        <v-col cols="12">

          <v-card class="progress-card">
            <v-card-text>
              <h2 class="progress-text">当前进度：{{ currentProblemIndex + 1 }}/{{ totalProblems }}</h2>
              <v-progress-linear :value="progressValue" color="green" class="progress-bar"></v-progress-linear>
            </v-card-text>
          </v-card>

          <v-form @submit.prevent="submitForm" v-if="question">
            <v-card class="large-card">
              <v-card-title>
                <h3>
                  {{ question.title }}
                </h3>
              </v-card-title>
              <v-card-text>
                <v-md-preview :text="question.content"></v-md-preview>
                <template v-if="question.type === 'SINGLE_CHOICE' && question.choices">
                  <v-radio-group v-model="answer">
                    <v-radio v-for="(choice, key) in question.choices" :key="key" :label="`${key}. ${choice}`"
                      :value="key" class="option-box" :class="{
                        'correct-answer': resultType === 'success' && answer === key,
                        'wrong-answer': resultType === 'error' && answer === key,
                        'disabled': resultMessage
                      }">
                      <template v-slot:label>
                        <v-icon v-if="resultType === 'success' && answer === key" class="correct-icon"
                          color="green">mdi-check-circle</v-icon>
                        <v-icon v-if="resultType === 'error' && answer === key" class="wrong-icon"
                          color="red">mdi-close-circle</v-icon>
                        {{ key }}. {{ choice }}
                      </template>
                    </v-radio>
                  </v-radio-group>
                </template>
                <template v-else-if="question.type === 'MULTI_CHOICE' && question.choices">
                  <v-checkbox v-for="(choice, key) in question.choices" :key="key" :label="`${key}. ${choice}`"
                    :value="key" v-model="selectedAnswers" @change="updateAnswers" class="option-box" :class="{
                      'correct-answer': resultType === 'success' && selectedAnswers.includes(key),
                      'wrong-answer': resultType === 'error' && selectedAnswers.includes(key),
                      'disabled': resultMessage
                    }">
                    <template v-slot:label>
                      <v-icon v-if="resultType === 'success' && selectedAnswers.includes(key)" class="correct-icon"
                        color="green">mdi-check-circle</v-icon>
                      <v-icon v-if="resultType === 'error' && selectedAnswers.includes(key)" class="wrong-icon"
                        color="red">mdi-close-circle</v-icon>
                      {{ key }}. {{ choice }}
                    </template>
                  </v-checkbox>
                </template>
                <template v-else-if="question.type === 'BLANK_FILLING'">
                  <v-text-field v-model="answer" label="填空"></v-text-field>
                </template>
              </v-card-text>
              <v-card-actions>
                <v-btn type="submit" color="success" class="green-button">
                  提交
                </v-btn>
                <v-btn v-if="resultMessage && !showAnswers" @click="fetchCorrectAnswers" color="success"
                  class="green-button">
                  显示答案
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn @click="previousProblem" class="navigation-button">
                  <span class="green-text">上一题</span>
                </v-btn>
                <v-btn @click="nextProblem" class="navigation-button">
                  <span class="green-text">下一题</span>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-form>
          <v-alert v-if="resultMessage" :type="resultType" class="mt-4 alert-large">
            {{ resultMessage }}
          </v-alert>
          <v-card v-if="correctAnswers && showAnswers" class="mt-4 answer-card-large">
            <v-card-title>
              <h3>
                参考答案
              </h3>
            </v-card-title>
            <v-card-text>
              <div v-if="question.type === 'SINGLE_CHOICE'">
                <ul>
                  <li v-for="(value, key) in correctAnswers" :key="key">{{ `${key}. ${value}` }}</li>
                </ul>
              </div>
              <div v-else-if="question.type === 'MULTI_CHOICE'">
                <ul>
                  <li v-for="(value, key) in correctAnswers" :key="key">{{ `${key}. ${value}` }}</li>
                </ul>
              </div>
              <div v-else-if="question.type === 'BLANK_FILLING'">
                <ul>
                  <li v-for="(answer, index) in correctAnswers" :key="index">{{ `${index}: ${answer}` }}</li>
                </ul>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

export default {
  props: {
    pid: {
      type: String,
      required: true,
    },
  },
  components: {
    VMdPreview,
  },
  data() {
    return {
      question: null,
      loading: true,
      selectedAnswers: [], // 用于多选题选项
      answer: '', // 用于单选题和填空题答案
      isSingleChoice: true,
      resultMessage: '',
      resultType: '',
      correctAnswers: null,
      showAnswers: false,
    };
  },
  computed: {
    currentProblemIndex() {
      return this.$store.state.currentProblemGroup.problems.findIndex(
        (problem) => problem.pid === this.pid
      );
    },
    totalProblems() {
      return this.$store.state.currentProblemGroup.problems.length;
    },
    progressValue() {
      return ((this.currentProblemIndex + 1) / this.totalProblems) * 100;
    },
  },
  created() {
    this.fetchQuestion();
  },
  watch: {
    '$route.params.pid': 'fetchQuestion',
  },
  methods: {
    fetchQuestion() {
      this.loading = true;
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
        })
        .finally(() => {
          this.loading = false;
        });
    },
    previousProblem() {
      const currentIndex = this.currentProblemIndex;
      if (currentIndex > 0) {
        const previousProblem = this.$store.state.currentProblemGroup.problems[currentIndex - 1];
        this.selectedAnswers = [];
        this.showAnswers = false;
        this.resultType = '';
        this.$router.push({ path: '' + previousProblem.pid });
      } else {
        this.$store.commit('setAlert', {
          type: 'warning',
          message: '现在已经是第一题',
        });
      }
    },
    nextProblem() {
      const currentIndex = this.currentProblemIndex;
      if (currentIndex < this.totalProblems - 1) {
        const nextProblem =
          this.$store.state.currentProblemGroup.problems[currentIndex + 1];
        this.selectedAnswers = [];
        this.showAnswers = false;
        this.resultType = '';
        this.$router.push({ path: '' + nextProblem.pid });
      } else {
        this.$store.commit('setAlert', {
          type: 'warning',
          message: '现在已经是最后一题',
        });
      }
    },
    getCurrentProblemIndex() {
      return this.$store.state.currentProblemGroup.problems.findIndex(
        (problem) => problem.pid === this.pid
      );
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
          this.hideAlertAfterDelay();
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
    hideAlertAfterDelay() {
      setTimeout(() => {
        this.resultMessage = ''; // 清除提示信息
      }, 4000); // 5秒后隐藏提示信息
    },
    returnback() {
      //this.$router.go(-1);
      this.$router.push('/exercises');
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

.navigation-button {
  background-color: transparent;
  color: inherit;
  border: none;
  font-size: 1.5em;
  box-shadow: none;
}

.large-card {
  width: 100%;
  max-width: 1900px;
  margin: 0 auto;
  padding: 20px;
}

.progress-card {
  width: 100%;
  max-width: 1900px;
  margin: 0 auto 20px;
  padding: 20px;
  background-color: #f5f5f5;
}

.progress-text {
  margin-bottom: 10px;
}

.progress-bar {
  height: 10px;
}


.option-box {
  display: flex;
  align-items: center;
  font-size: 24px;
  margin: 10px 0;
}

.correct-answer {
  background-color: #31bc51;
}

.wrong-answer {
  background-color: #f8d7da;
}

.correct-icon {
  color: #28a745;
  margin-right: 10px;
}

.wrong-icon {
  color: #dc3545;
  margin-right: 10px;
}

.text-field-large {
  font-size: 24px;
  height: 60px;
}

.green-button {
  background-color: #4caf50;
  color: white;
  border-radius: 10px;
  font-size: 30px;
  padding: 30px 50px;
  margin-right: 10px;
  min-width: 150px;
  height: 600;
}

.alert-large {
  font-size: 20px;
}

.answer-card-large {
  background-color: #28a745;

  width: 100%;
  max-width: 1900px;
  margin: 0 auto;
  padding: 20px;
}

.mt-4 {
  margin-top: 16px;
}

.disabled {
  pointer-events: none;
}
</style>
