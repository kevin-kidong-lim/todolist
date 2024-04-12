import axios from "axios";
// import withTokenAxios from "@/axios/withTokenAxios"
import withTokenAxios from "@/axios/withTokenAxios"
export function userLogin(userData) {
    return axios.post('/api/member/token/', userData);
}
export function findPassword(userData) {
    return axios.post('/api/member/findpassword/', userData);
}

export const getRequestApi = (endPoint, userData) =>{
    return axios.get(endPoint, userData);
}
export const postMultipartRequestApi = (endPoint, userData) => {
    return axios.post(endPoint, userData, {
        headers: {
          "Content-Type": "multipart/form-data", 
        },
      });
}
export const postRequestApi = (endPoint, userData) => {
    return axios.post(endPoint, userData);
}
export const fetchRequestApi = (endPoint, userData) => {
    return axios.fetch(endPoint, userData);
}
export const postRequestWithAuthApi = (endPoint, userData) => {
    return withTokenAxios.post(endPoint, userData);
}
export const putRequestWithAuthApi = (endPoint, userData) => {
    return withTokenAxios.put(endPoint, userData);
}
export const putMultipartRequestWithAuthApi = (endPoint, userData) => {
    return withTokenAxios.put(endPoint, userData, {
        headers: {
          "Content-Type": "multipart/form-data", 
        },
      });
}
export const postMultipartRequestWithAuthApi = (endPoint, userData) => {
    return withTokenAxios.post(endPoint, userData, {
        headers: {
          "Content-Type": "multipart/form-data", 
        },
      });
}
export const getRequestWithAuthApi = (endPoint, params) => {
    return withTokenAxios.get(endPoint, { params });
  };
export const deleteRequestWithAuthApi = (endPoint, userData) => {
    return withTokenAxios.delete(endPoint, userData);
}
export const patchRequestWithAuthApi = (endPoint, userData) => {
    return withTokenAxios.patch(endPoint, userData);
}