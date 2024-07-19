<template>
  <v-container
    class="spacing-playground pa-6"
    fluid
  >
    <news />
    <!-- <v-row>
      <v-col
        class="d-flex align-center"
        cols="12"
        sm="6"
      >
        <v-select
          v-model="paddingDirection"
          :items="directions"
          class="pr-2"
          label="Padding"
        >
          <template v-slot:prepend>
            <strong class="primary--text py-1">p</strong>
          </template>

          <template v-slot:append-outer>
            <div class="py-1">
              -
            </div>
          </template>
        </v-select>

        <v-select
          v-model="paddingSize"
          :items="paddingSizes.slice(1)"
          label="Size"
        ></v-select>
      </v-col>

      <v-col
        class="d-flex"
        cols="12"
        sm="6"
      >
        <v-select
          v-model="marginDirection"
          :items="directions"
          class="pr-2"
          label="Margin"
        >
          <template v-slot:prepend>
            <strong class="primary--text py-1">m</strong>
          </template>

          <template v-slot:append-outer>
            <div class="py-1">
              <news />
            </div>
          </template>
        </v-select>

        <v-select
          v-model="marginSize"
          :items="marginSizes"
          label="Size"
        ></v-select>
      </v-col>

      <v-col
        class="orange lighten-3 pa-0"
        cols="12"
      >
        <v-sheet
          :class="[computedMargin]"
          elevation="4"
          rounded
        >
          <div
            :class="[computedPadding]"
            class="light-green lighten-3"
          >
            <div
              class="white text-center py-6"
              v-text="playgroundText"
            ></div>
          </div>
        </v-sheet>
      </v-col>
    </v-row> -->
  </v-container>
</template>

<script>
import news from '../components/NewsList.vue'

export default {
  name: 'HomeView',
  components: {
    news
  }
}

</script>
