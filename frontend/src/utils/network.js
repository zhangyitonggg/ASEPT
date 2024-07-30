import axios from "axios";
import qs from "qs";
import store from "../store";

const handle400 = (info) => {
  if (info.detail) {
    switch (info.detail) {
      case "Contains sensetive words":
        return "对不起。看起来你的输入包含了敏感词汇。请检查输入再试。";
      default:
        return info.detail;
    }
  } else {
    return "对不起。看起来你遇到了一些问题。";
  }
}

const errorHandle = (status, info) => {
  switch (status) {
    case 400:
      return handle400(info);
    case 401:
      return "对不起。看起来你没有对应的权限。";
    case 403:
      return "对不起。看起来你的令牌已经过期。请重新登录。";
    case 404:
      return "对不起。看起来你迷路了。";
    case 408:
      return "请求错误。";
    case 422:
      return "对不起。看起来你的请求格式出了点错误。重新检查一下你的输入？";
    case 500:
      return "对不起。看起来我们的服务器出了一些问题。";
    case 501:
      return "对不起。看起来这个服务还没有实现。";
    case 502:
      return "对不起。看起来你的网络配置出了一些问题。";
    case 503:
      return "对不起。看起来这个服务暂时不可用。我们正在紧急维护，请稍等。";
    default:
      return "对不起。看起来你遇到了一些问题。这可能是我们导致的问题。请检查你的网络配置，或者与管理员联系。";
  }
};


const router = axios.create({
  timeout: 6000,
});


router.interceptors.request.use(
  config => {
    if (config.method === 'post') {
      if (config.useQs) {
        config.data = qs.stringify(config.data);
        config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      } else if (config.useMultipart) {
        config.headers['Content-Type'] = 'multipart/form-data';
        config.timeout = 120000;
      } else {
        config.headers['Content-Type'] = 'application/json';
      }
    }
    const token = store.state._token_;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      config.params = {
        ...config.params,
        authorized_user_name: store.getters.username
      };
    }
    console.log(config);
    return config;
  },
  error => {
    return Promise.reject(error);
  }
)

router.interceptors.response.use(
  response => {
    if (response.status === 200) {
      return Promise.resolve(response);
    } else {
      return Promise.reject(response);
    }
  },
  error => {
    const { response } = error;
    try {
      return Promise.reject(errorHandle(response.status, response.data));
    } catch (e) {
      return Promise.reject("对不起。我们遇到了一些未知的问题。");
    }
  }
)

export default router;