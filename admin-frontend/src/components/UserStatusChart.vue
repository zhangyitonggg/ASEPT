<template>
  <div>
    <Pie :data="datacollection" :options="options"></Pie>
  </div>
</template>

<script>
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

export default {
  components: {
    Pie
  },
  props: {
    passedQuestions: {
      type: Number,
      required: true
    },
    failedQuestions: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      datacollection: {
        labels: ['Passed Questions', 'Failed Questions'],
        datasets: [
          {
            backgroundColor: [
              '#4CAF50',
              '#FF0000'
            ],
            data: [
              this.passedQuestions,
              this.failedQuestions
            ]
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  watch: {
    passedQuestions() {
      this.updateChart()
    },
    failedQuestions() {
      this.updateChart()
    }
  },
  methods: {
    updateChart() {
      this.datacollection.datasets[0].data = [this.passedQuestions, this.failedQuestions]
    }
  },
  mounted() {
    this.updateChart()
  }
}
</script>

<style scoped>
div {
  max-width: 500px;
  margin: 0 auto;
}
</style>