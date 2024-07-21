import axios from "axios";
import qs from "qs";
import store from "../store";

const errorHandle = (status, info) => {
    switch (status) {
        case 400:
            console.log("请求错误");
            break;
        case 401:
            console.log("未授权，请登录");
            break;
        case 403:
            console.log("拒绝访问");
            break;
        case 404:
            console.log("请求地址出错");
            break;
        case 408:
            console.log("error408");
            break;
        case 500:
            console.log("服务器内部错误");
            break;
        case 501:
            console.log("服务未实现");
            break;
        case 502:
            console.log("网关错误");
            break;
        case 503:
            console.log("服务不可用");
            break;
        default:
            console.log(info);
            break;
    }
};


const router = axios.create({
    timeout: 3000,
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
    },
});


router.interceptors.request.use(
    config => {
        if (config.method === 'post') {
            config.data = qs.stringify(config.data);
        }
        const token = store.state._token_;
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
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
        console.log(error);
        const { response } = error;
        errorHandle(response.status, response.info);
    }
)

export default router;