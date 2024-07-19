import router from "../utils/network";
import path from "./path";
import { qs } from "qs";

const api = {
    login: async (username, password) => {
        const response = await router.post(path.baseUrl + path.login, {
            username: username,
            password: password
        });
        return response;
    },
};

export default api;