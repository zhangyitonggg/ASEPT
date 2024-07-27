<template>
  <v-card
    class="mt-4 mx-auto"
    v-if="total_passed > 0"
    max-width="80%"
  >
    <v-sheet
      class="v-sheet--offset mx-auto"
      elevation="12"
      max-width="calc(100% - 32px)"
    >
    <v-card>
      <v-card-title>
        <v-icon
          class="mr-8"
          size="64"
        > mdi-check-all
        </v-icon>
        <v-row align="start">
          <div class="text-caption grey--text text-uppercase">
            总通过题数
          </div>
          <div>
            <span
              class="text-h3 font-weight-black"
              v-text="`${total_passed}`"
            ></span>
          </div>
        </v-row>
      </v-card-title>

      <v-sheet color="transparent">
        <v-sparkline
          :labels="labels"
          :value="values"
          show-labels="true"
          auto-draw="true"
          label-size="3"
          :gradient="gradient"
          line-width="1"
          :aspect-ratio="16/9"
          class="mx-auto"
          padding="24"
          gradient-direction="bottom"
        ></v-sparkline>
      </v-sheet>
    </v-card>
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
    total_passed: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      gradient: ['#FFEBEE', '#D50000'],
    };
  },
}
</script>

<style>
  .v-sheet--offset {
    top: -24px;
    position: relative;
  }

  /* 假设标签包含在具有 'sparkline-label' 类的元素中 */
  .sparkline-label {
    transform: rotate(-45deg);
    transform-origin: top right; /* 调整旋转的基点为顶部右侧 */
    margin-right: 5px; /* 可能需要调整间距来避免标签重叠 */
    white-space: nowrap; /* 防止标签文字折行 */
  }
</style>