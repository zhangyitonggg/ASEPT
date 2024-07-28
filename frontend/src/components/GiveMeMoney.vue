<template>
  <v-container>
    <v-card class="mb-10">
      <v-card-title>
        <h2>我很可爱，请给我钱！</h2>
      </v-card-title>
      <v-card-text>
        <v-img src="../assets/images/wxmoney.jpg" max-height="600" max-width="250" contain></v-img>
        <v-img src="../assets/images/zfbmoney.jpg" max-height="600" max-width="250" contain></v-img>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'MoneyMoney',
  data() {
    return {
    };
  },
  mounted() {
    this.$store.commit('setAppTitle', '支持我们');
  },
};
</script>