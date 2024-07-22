import router from "../utils/network";
import path from "./path";
import { qs } from "qs";

const api = {
    login: async(username, password) => {
        const response = await router.post(path.baseUrl + path.login, {
            username: username,
            password: password
        });
        return response;
    },
    getnews: async() => {
        const response = await router.get(path.baseUrl + path.news_getannouncements);
        return response;
    },
    register: async(username, password) => {
      console.log("register");
      console.log(username, password);
      return await router.post(path.baseUrl + path.logon, {
        username: username,
        password: password
      });
    },
};

export default api;