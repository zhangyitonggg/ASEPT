<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>这些设置控制网页的全局功能。注意，这些设置只在此设备上有效。</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-col>
          <v-switch inset v-model="$vuetify.theme.dark" label="启用黑暗模式" @click="handleDarkTheme" />
        </v-col>
        <v-col>
          <v-switch inset v-model="particles" label="开启背景颗粒" @click="handleParticles" />
        </v-col>  
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      particles: false,
    }
  },
  methods: {
    handleDarkTheme() {
      this.$store.commit("setAlert", this.$vuetify.theme.dark ? { "type": "success", "message": "黑暗模式已启用。" } : { "type": "success", "message": "黑暗模式已关闭。" });
      localStorage.setItem("__dark_theme__", this.$vuetify.theme.dark);
    },
    handleParticles() {
      this.$store.commit("setParticles", this.particles);
      this.$store.commit("setAlert", this.particles ? { "type": "success", "message": "背景颗粒已启用。" } : { "type": "success", "message": "背景颗粒已关闭。" });
    }
  },
  created() {
    this.particles = this.$store.getters.particles;
  }
}
</script>
