<template>
    <div class="news-container">
      <h1>近期新闻</h1>
      <div v-for="article in articles" :key="article.id" class="news-item">
        <h2>{{ article.title }}</h2>
          <p>{{article.content}}</p>
          <p class="author">author: {{article.author}}</p>
        
        <a :href="article.url" target="_blank" class="read-more">阅读更多</a>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'

  export default {
    data() {
      return {
        names: 'News',
        articles: [
          // {
          //   id: 1,
          //   title: '魏佬为什么不睡觉',
          //   description: '据yt日报报道，魏佬已经很久没睡觉了，原因竟是他在学Vue',
          //   url: 'https://weixinvcci.github.io/'
          // },
          // {
          //   id: 2,
          //   title: '我爱北航',
          //   description: '北航也是一个好学校————xxx',
          //   url: 'https://www.tsinghua.edu.cn/'
          // },
          // {
          //   id: 3,
          //   title: '大家都很喜欢python',
          //   description: '据说有很多人喜欢python',
          //   url: 'https://course.educg.net/indexcs/simple.jsp?loginErr=0'
          // }
          // // 可以添加更多新闻条目
        ]
      };
    },
    mounted() {
      this.getAnnouncement();
    },
    methods: {
        getAnnouncement() {
          axios.get('http://localhost:8000/news/get_announcements',{
            params: {
              max_announcements: 3
            }
          })
          .then(
            response => {
              const announcements = response.data;
              console.log('response received:',response.data);
              this.articles = response.data.announcements;
            })
          .catch(error => {
               console.error('There was an error fetching the announcements:', error);
          });
            
        },
    }
  };
  </script>
  
  <style scoped>
  .news-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .news-item {
    margin-bottom: 20px;
    width:300px;
    padding: 15px;
    background-color: #f0f0f0;
    border-radius: 5px;
  }
  
  .news-item h2 {
    margin-bottom: 10px;
  }
  
  .read-more {
    display: inline-block;
    padding: 5px 10px;
    background-color: #007bff;
    color: #fff;
    text-decoration: none;
    border-radius: 3px;
    transition: background-color 0.3s ease;
  }
  
  .read-more:hover {
    background-color: #0056b3;
  }

  .author {
    font-size:13px;
    color:grey;
  }
  </style>
  