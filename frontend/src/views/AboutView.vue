<template>
  <v-container>
    <v-card class="mb-10">
      <v-card-title>
        <h2>关于平台</h2>
      </v-card-title>
      <v-card-text>
        <div>
          这是 ASEPT（A Shared Exercise PlaTform），一个用于分享题目和自主练习的平台。
        </div>
      </v-card-text>
    </v-card>
    <v-card>
      <v-card-title>
        <h2>关于项目</h2>
      </v-card-title>
      <v-card-text>
        <div>
          这是一个基于 Vue2 和 FastAPI 的开源项目。
          <br />
          项目代码托管于 <a href="https://github.com/zhangyitonggg/Shared-Exercise-Platform">GitHub</a>。
          <br />
          你所看到的页面渲染于 {{ new Date().toLocaleString() }}。
        </div>
        <br />
        <div>
          我们会不定期推出更新的版本来提升你的使用体验。如果你刷新页面后发现内容发生了变化，说明你的浏览器可能正在使用缓存内容渲染。
          <br />
          通常来说，缓存会在一段时间后自动更新。如果需要，请手动清理浏览器的缓存。
        </div>
        <br />
        <div>
          本项目的诞生离不开包括 Vue 和 Node.js 在内的众多开源项目。
        </div>
        <br>
        <div>
          感谢所有人对该项目提供的帮助。以下是项目的主要贡献者：
        </div>
        <br />
        <v-row>
          <v-col v-for="contributor in contributors" :key="contributor.id">
            <v-avatar size="50" :color="contributor.site_admin ? 'red' : 'blue'">
              <img :src="contributor.avatar_url" />
            </v-avatar>
            <h4>
              <a :href="contributor.html_url">{{ contributor.login }}</a>
            </h4>
            <p>贡献次数：{{ contributor.contributions }}</p>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'AboutView',
  data() {
    return {
      loading: false,
      contributors: [
        {
          "login": "AOSTL",
          "id": 60469446,
          "node_id": "MDQ6VXNlcjYwNDY5NDQ2",
          "avatar_url": "https://avatars.githubusercontent.com/u/60469446?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/AOSTL",
          "html_url": "https://github.com/AOSTL",
          "followers_url": "https://api.github.com/users/AOSTL/followers",
          "following_url": "https://api.github.com/users/AOSTL/following{/other_user}",
          "gists_url": "https://api.github.com/users/AOSTL/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/AOSTL/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/AOSTL/subscriptions",
          "organizations_url": "https://api.github.com/users/AOSTL/orgs",
          "repos_url": "https://api.github.com/users/AOSTL/repos",
          "events_url": "https://api.github.com/users/AOSTL/events{/privacy}",
          "received_events_url": "https://api.github.com/users/AOSTL/received_events",
          "type": "User",
          "site_admin": false,
          "contributions": 40
        },
        {
          "login": "jhdonghj",
          "id": 36978310,
          "node_id": "MDQ6VXNlcjM2OTc4MzEw",
          "avatar_url": "https://avatars.githubusercontent.com/u/36978310?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/jhdonghj",
          "html_url": "https://github.com/jhdonghj",
          "followers_url": "https://api.github.com/users/jhdonghj/followers",
          "following_url": "https://api.github.com/users/jhdonghj/following{/other_user}",
          "gists_url": "https://api.github.com/users/jhdonghj/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/jhdonghj/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/jhdonghj/subscriptions",
          "organizations_url": "https://api.github.com/users/jhdonghj/orgs",
          "repos_url": "https://api.github.com/users/jhdonghj/repos",
          "events_url": "https://api.github.com/users/jhdonghj/events{/privacy}",
          "received_events_url": "https://api.github.com/users/jhdonghj/received_events",
          "type": "User",
          "site_admin": false,
          "contributions": 14
        }
      ],
    };
  },
  mounted() {
    this.$store.commit('setAppTitle', '关于');
  },
};
</script>