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

    <!-- <v-btn
    class="navigation-button"
    fab
    dark
    color="primary"
    @click="previousQuestion"
    :disabled="!hasPrevious"
  >
    <v-icon dark>mdi-chevron-left</v-icon>
  </v-btn> -->

  <!-- 下一题按钮 -->
  <!-- <v-btn
    class="navigation-button"
    fab
    dark
    color="primary"
    @click="nextQuestion"
    :disabled="!hasNext"
  >
    <v-icon dark>mdi-chevron-right</v-icon>
  </v-btn> -->

    <v-row justify="center">
      <v-col cols="12">
        <v-form @submit.prevent="submitForm" v-if="question">
          <v-card class="large-card">
            <v-card-title class="text-h3">{{ question.title }}</v-card-title>
            <v-card-text>
              <p class="text-h5">{{ question.content }}</p>
              <template v-if="question.type === 'SINGLE_CHOICE' && question.choices">
                <v-radio-group v-model="answer">
                  <v-radio
                    v-for="(choice, key) in question.choices"
                    :key="key"
                    :label="`${key}. ${choice}`"
                    :value="key"
                    class="option-box"
                    :class="{
                      'correct-answer': resultType === 'success' && answer === key,
                      'wrong-answer': resultType === 'error' && answer === key,
                      'disabled': resultMessage // 禁用选项交互
                    }"
                  >
                    <template v-slot:label>
                      <v-icon
                        v-if="resultType === 'success' && answer === key"
                        class="correct-icon"
                        color="green"
                      >mdi-check-circle</v-icon>
                      <v-icon
                        v-if="resultType === 'error' && answer === key"
                        class="wrong-icon"
                        color="red"
                      >mdi-close-circle</v-icon>
                      {{ key }}. {{ choice }}
                    </template>
                  </v-radio>
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
                  class="option-box"
                  :class="{
                    'correct-answer': resultType === 'success' && selectedAnswers.includes(key),
                    'wrong-answer': resultType === 'error' && selectedAnswers.includes(key),
                    'disabled': resultMessage // 禁用选项交互
                  }"
                >
                  <template v-slot:label>
                    <v-icon
                      v-if="resultType === 'success' && selectedAnswers.includes(key)"
                      class="correct-icon"
                      color="green"
                    >mdi-check-circle</v-icon>
                    <v-icon
                      v-if="resultType === 'error' && selectedAnswers.includes(key)"
                      class="wrong-icon"
                      color="red"
                    >mdi-close-circle</v-icon>
                    {{ key }}. {{ choice }}
                  </template>
                </v-checkbox>
              </template>
              <template v-else-if="question.type === 'BLANK_FILLING'">
                <v-text-field
                  v-model="answer"
                  label="填空"
                  class="text-field-large"
                ></v-text-field>
              </template>
            </v-card-text>
            <v-card-actions>
              <v-btn
                type="submit"
                color="success"
                class="green-button"
              >
                提交
              </v-btn>
              <v-btn
                v-if="resultMessage && !showAnswers"
                @click="fetchCorrectAnswers"
                color="success"
                class="green-button"
              >
                显示答案
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
        <v-alert v-if="resultMessage" :type="resultType" class="mt-4 alert-large">
          {{ resultMessage }}
        </v-alert>
        <v-card v-if="correctAnswers && showAnswers" class="mt-4 answer-card-large">
          <v-card-title class="text-h3">正确答案</v-card-title>
          <v-card-text>
            <div v-if="question.type === 'SINGLE_CHOICE'">
              <p class="text-h5">正确选项:</p>
              <ul>
                <li v-for="(value, key) in correctAnswers" :key="key" class="text-h5">{{ `${key}. ${value}` }}</li>
              </ul>
            </div>
            <div v-else-if="question.type === 'MULTI_CHOICE'">
              <p class="text-h5">正确选项:</p>
              <ul>
                <li v-for="(value, key) in correctAnswers" :key="key" class="text-h5">{{ `${key}. ${value}` }}</li>
              </ul>
            </div>
            <div v-else-if="question.type === 'BLANK_FILLING'">
              <p class="text-h5">正确答案:</p>
              <ul>
                <li v-for="(answer, index) in correctAnswers" :key="index" class="text-h5">{{ `${index}: ${answer}` }}</li>
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
      hasPrevious: false,
      hasNext: false,
      //allQuestions: [], // 所有题目列表
    };
  },
  created() {
   // this.fetchAllQuestions();
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
    // fetchAllQuestions() {
    //   console.log('qqq: ',this.$store.state.problems);
    //   this.allQuestions =  this.$store.state.problems;
    //   console.log(this.allQuestions);
    //   this.updateNavigation();
    // },
    // updateNavigation() {
    //   const currentIndex = this.allQuestions.findIndex(q => q.pid === this.pid);
    //   this.hasPrevious = currentIndex > 0;
    //   this.hasNext = currentIndex < this.allQuestions.length - 1;
    // },
    // previousQuestion() {
    //   const currentIndex = this.allQuestions.findIndex(q => q.pid === this.pid);
    //   if (this.hasPrevious) {
    //     this.$router.push({ path: `/exercises/solve/${this.allQuestions[currentIndex - 1].pid}` });
    //   }
    // },
    // nextQuestion() {
    //   const currentIndex = this.allQuestions.findIndex(q => q.pid === this.pid);
    //   if (this.hasNext) {
    //     this.$router.push({ path: `/exercises/solve/${this.allQuestions[currentIndex + 1].pid}` });
    //   }
    // },
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
.navigation-button {
  position: fixed;
  bottom: 20%;
  z-index: 5;
  font-size: 30px;
  width: 60px;
  height: 60px;
}

.navigation-button:nth-of-type(1) {
  left: 10%;
}

.navigation-button:nth-of-type(2) {
  right: 10%;
}

.large-card {
  width: 100%;
  max-width: 1900px;
  margin: 0 auto;
  padding: 20px;
}

.option-box {
  display: flex;
  align-items: center;
  height: 80px;
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
