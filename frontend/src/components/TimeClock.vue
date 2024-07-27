<template>
  <div>{{ formattedTime }}</div>
</template>

<script>
import api from '@/api';

export default {
  data: () => ({
    serverTime: new Date(),
    formattedTime: ''
  }),
  created() {
    this.fetchTime();
    this.timer = setInterval(this.updateTime, 1000);
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    fetchTime() {
      const response = api.getTime()
        .then(response => {
          console.log(response);
          this.serverTime = new Date(response.data.current_time);
          this.formattedTime = this.formatDateTime(this.serverTime);
        })
        .catch(() => {
          this.$store.commit('setAlert', { message: '无法获取服务器时间。', type: 'error' });
        });
    },
    updateTime() {
      this.serverTime.setSeconds(this.serverTime.getSeconds() + 1);
      this.formattedTime = this.formatDateTime(this.serverTime);
    },
    formatDateTime(date) {
      return `${date.getFullYear()}-${this.pad2(date.getMonth() + 1)}-${this.pad2(date.getDate())} ${this.pad2(date.getHours())}:${this.pad2(date.getMinutes())}:${this.pad2(date.getSeconds())}`;
    },
    pad2(number) {
      return (number < 10 ? '0' : '') + number;
    }
  }
}
</script>
