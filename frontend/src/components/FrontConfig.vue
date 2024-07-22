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
          <v-switch
          inset
          v-model="darkTheme"
          label="启用黑暗模式"
          />
        </v-col>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Component, Watch, Vue } from 'vue-property-decorator'

export default{
  data() {
    return {
      darkTheme: false
    }
  }

  // @Watch('$vuetify.theme.dark')
  // triggersUpdateDarkThemeLocalValue() {
  //   if (this.darkThemeFollowsSystem) return
  //   // @ts-ignore
  //   localStorage.setItem('dark', String(this.$vuetify.theme.dark))
  // }
}
</script>
