<template>
  <v-list dense>
    <v-list-item 
      v-for="post in posts" 
      :key="post.id" 
      @click="selectPost(post)"
    >
      <v-list-item-content>
        <v-list-item-title>{{ post.title }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: 'PostsList',
  data() {
    return {
      posts: [
          {
            id: 111,
            title: 'Post Title'
          },
          {
            id: 222,
            title: 'Another Post Title',
          }
      ],
    }
  },
  props: {
  },
  methods: {
    selectPost(post) {
      // this.$emit('select', post);
    }
  },
  mounted() {
    this.$store.commit('setAppTitle', '水吧');
  }
}
</script>