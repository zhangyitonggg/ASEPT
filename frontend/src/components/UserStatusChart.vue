<template>
  <Pie :data="datacollection" :options="options" />
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
    data: {
      type: Array,
      required: true
    },
    labels: {
      type: Array,
      required: true
    },
    backgroundColor: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      datacollection: {
        labels: this.labels,
        datasets: [
          {
            backgroundColor: this.backgroundColor,
            data: this.data
          }
        ]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: this.title, // 使用 prop 传入的 title
            font: {
              size: 16, // 新 API 用 font.size 替代 fontSize
              family: 'Arial' // 新 API 用 font.family 替代 fontFamily
            },
            padding: 20,
            position: 'top'
          },
          legend: {
            display: true,
            position: 'bottom'
          }
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  watch: {
  },
  methods: {
  },
  mounted() {
  }
}
</script>

<style scoped>
div {
  max-width: 500px;
  margin: 0 auto;
}
</style>