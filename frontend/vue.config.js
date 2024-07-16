module.exports = {
  pages: {
    index: {
      //入口
      entry: 'src/main.js',
    },
  },
	lintOnSave:false, //关闭语法检查

  devServer: {
    // proxy: "http://localhost:8000/" 
    proxy: {
      '/login': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        pathRewrite:{'^/login':''},
        // ws: true, //用于支持websocket
        // changeOrigin: true //用于控制请求头中的host值
      },
      '/register': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        pathRewrite:{'^/register':''},
      },
    }
  }
}