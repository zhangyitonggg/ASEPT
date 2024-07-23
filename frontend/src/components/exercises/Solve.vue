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

    <v-form @submit.prevent="submitForm" v-if="question">
      <v-card class="mb-4">
        <v-card-title>{{ question.title }}</v-card-title>
        <v-card-text>
          <p>{{ question.content }}</p>
          <template v-if="question.type === 'CHOICE' && question.choices">
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
            <v-text-field v-for="(blank, index) in question.answers"
                          :key="index"
                          v-model="answer[index]"
                          :label="`Blank ${index + 1}`"></v-text-field>
          </template>
        </v-card-text>
      </v-card>
      <v-btn type="submit" color="primary">Submit</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      question: null,
      answer: {},
      isSingleChoice: true,
    };
  },
  created() {
    this.fetchQuestion();
  },
  methods: {
    fetchQuestion() {
      let pid = 0;
      this.$store
      .dispatch('getProblemById',pid)
      .then(res => {
       
        this.question = {
          pid: res.data.pid,
          title: res.data.title,
          content: res.data.content,
          type: res.data.type,
          author: res.data.author,
          update_time: res.data.update_time,
          is_published: res.data.is_published,
          choices: this.parseChoices(res.data.choices),
          answers: this.parseAnswers(res.data.answers),
        };
        this.isSingleChoice = this.question.answers && Object.keys(this.question.answers).length === 1;
      })
      .catch(error => {
             this.$store.commit("setAlert", {
             type: "error",
            message: error,
          });
          }).finally(() => {
          this.loading = false;
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
      return null;
    },
    submitForm() {
      console.log(this.answer);
      alert(JSON.stringify(this.answer, null, 2));
    },
    returnback() {
      this.$router.go(-1);
    }
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
.mb-4 {
  margin-bottom: 1rem;
}
</style>



























<!-- <template>
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
   

    <v-form @submit.prevent="submitForm">
      <v-card v-for="(question, index) in questions" :key="index" class="mb-4">
        <v-card-title>{{ question.title }}</v-card-title>
        <v-card-text>
          <template v-if="question.type === 'single-choice'">
            <v-radio-group v-model="answers[index]">
              <v-radio
                v-for="(choice, cIndex) in question.choices"
                :key="cIndex"
                :label="`${getOptionLabel(cIndex)}. ${choice}`"
                :value="choice"
              ></v-radio>
            </v-radio-group>
          </template>
          <template v-else-if="question.type === 'multiple-choice'">
            <v-checkbox-group v-model="answers[index]">
              <v-checkbox
                v-for="(choice, cIndex) in question.choices"
                :key="cIndex"
                :label="`${getOptionLabel(cIndex)}. ${choice}`"
                :value="choice"
              ></v-checkbox>
            </v-checkbox-group>
          </template>
          <template v-else-if="question.type === 'fill-in-the-blank'">
            <v-text-field v-model="answers[index]" label="Your Answer"></v-text-field>
          </template>
        </v-card-text>
      </v-card>
      <v-btn type="submit" color="primary">Submit</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      questions: [
        {
          title: "What is the capital of France?",
          type: "single-choice",
          choices: ["Paris", "London", "Rome", "Berlin"],
        },
        {
          title: "Select the prime numbers.",
          type: "multiple-choice",
          choices: ["2", "3", "4", "5"],
        },
        {
          title: "Fill in the blank: 2 + 2 =",
          type: "fill-in-the-blank",
        },
      ],
      answers: {},
    };
  },
  methods: {
    getOptionLabel(index) {
      return String.fromCharCode(65 + index); // 65 is the char code for 'A'
    },
    submitForm() {
      console.log(this.answers);
      alert(JSON.stringify(this.answers, null, 2));
    },
    handleButtonClick() {
      alert('Button clicked!');
    },
    returnback() {
      this.$router.go(-1);
    }
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
.mb-4 {
  margin-bottom: 1rem;
}
</style> -->