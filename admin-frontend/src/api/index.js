import router from "../utils/network";
import path from "./path";
import { qs } from "qs";

const api = {
    login: async(username, password) => {
        const response = await router.post(path.baseUrl + path.login, {
            username: username,
            password: password
        }, {
          useQs: true
        });
        return response;
    },
    getnews: async() => {
        const response = await router.get(path.baseUrl + path.news_getannouncements);
        return response;
    },
    showJoinedGroups: async() => {
      return await router.get(path.baseUrl + path.showJoinedGroups);
    },
    publishAnnouncement: async(title, content) => {
      return await router.post(path.baseUrl + path.publishAnnouncement, {
        title: title,
        content: content
      });
    },
    modifyAnnouncement: async(aid, title, content, is_active) => {
      return await router.post(path.baseUrl + path.modifyAnnouncement, {
        aid: aid,
        title: title,
        content: content,
        is_active: is_active,
      });
    }
};

export default api;