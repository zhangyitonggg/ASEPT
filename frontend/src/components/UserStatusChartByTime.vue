<template>
  <v-card
    class="mt-4 mx-auto"
    max-width="60%"
  >
    <v-sheet
      class="v-sheet--offset mx-auto"
      elevation="12"
      max-width="calc(100% - 32px)"
    >
      <v-sparkline
        :labels="labels"
        :value="values"
        line-width="2"
        padding="16"
      ></v-sparkline>
    </v-sheet>

    <v-card-text class="pt-0">
      <v-divider class="my-2"></v-divider>
      <v-icon
        class="mr-2"
        small
      > mdi-clock
      </v-icon>
      <span class="subheading font-weight-light grey--text">最后一次提交于 {{ this.lastUpdateTime }}。</span>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    lastUpdateTime: {
      type: String,
      required: true,
    },
    labels: {
      type: Array,
      required: true,
    },
    values: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style>
  .v-sheet--offset {
    top: -24px;
    position: relative;
  }
</style>