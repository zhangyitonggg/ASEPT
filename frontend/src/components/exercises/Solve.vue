<template>
  <v-container>
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
        if(index >= 26) return index - 26;
        else return String.fromCharCode(65 + index); // 65 is the char code for 'A'
    },
    submitForm() {
      console.log(this.answers);
      alert(JSON.stringify(this.answers, null, 2));
    },
  },
};
</script>

<style>
.mb-4 {
  margin-bottom: 1rem;
}
</style>

<!-- <template>
    <div>
        66666<br/>
        {{content}}
    </div>
</template>

<script>
    export default{
        data() {
            return {
                content:'',
                id:-1,
            }
        },
        mounted() {
            this.id = this.$store.problemid;
            //this.getProblme(id);
        },
        methods: {
            getProblem(id) {
                //补充交互功能
            },
        }
    }
</script> -->