

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
      this.$store
        .dispatch('getCorrectAnswersById', this.pid) // 请求正确答案
        .then(res => {
          const correctAnswers = this.parseAnswers(res.data);
          let isCorrect = false;

          if (this.question.type === 'SINGLE_CHOICE') {
            if (this.isSingleChoice) {
              isCorrect = Object.keys(correctAnswers)[0] === this.answer;
            } else {
              isCorrect = Array.isArray(this.answer) && this.answer.length === correctAnswers.length && this.answer.every(val => Object.values(correctAnswers).includes(val));
            }
          } else if (this.question.type === 'FILL_BLANK') {
            isCorrect = Object.keys(this.answer).length === correctAnswers.length &&
                        Object.keys(this.answer).every((key, index) => this.answer[key] === correctAnswers[index]);
          }

          if (isCorrect) {
            this.resultMessage = '回答正确';
            this.errorMessage = '';
          } else {
            this.resultMessage = '';
            this.errorMessage = '回答错误';
          }

          this.correctAnswers = correctAnswers;
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
