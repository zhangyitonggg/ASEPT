<template>
<div class="d-flex flex-column align-center justify-center" style="height: 100vh;">
    <v-container class="text-center">
    <v-row justify="center">
        <v-img
        src="../assets/images/404.png"
        max-width="200"
        max-height="200"
          >
            <template v-slot:placeholder>
              <v-row
                class="fill-height ma-0"
                align="center"
                justify="center"
              >
                <v-progress-circular
                  indeterminate
                  color="grey lighten-5"
                ></v-progress-circular>
              </v-row>
            </template>
          </v-img>
        <v-col cols="4" justify="center">
            <h1>404 - Page Not Found</h1>
            <p>Sorry, the page you are looking for does not exist.</p>
            <v-btn color="primary" @click="goHome">返回首页。</v-btn>
        </v-col>
    </v-row>
    </v-container>
</div>
</template>

<script>
export default {
name: "NotFound",
methods: {
    goHome() {
    this.$router.push({ path: '/' });
    }
}
}
</script>

<style scoped>
body {
margin: 0;
}
</style>