
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
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props:{
    pid: {
      type: String,
      require:true,
    }
  },
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
      this.$store
        .dispatch('getProblemById', this.pid)
        .then(res => {
          console.log('res:', res);
          this.question = {
            pid: res.pid,
            title: res.title,
            content: res.content,
            type: res.type,
            author: res.author,
            update_time: res.update_time,
            is_public: res.is_public,
            choices: this.parseChoices(res.choices),
            answers: this.parseAnswers(res.answers),
            
          };
          console.log(this.question.choices);
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
