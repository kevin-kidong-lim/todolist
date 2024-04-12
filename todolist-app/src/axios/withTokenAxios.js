import axios from "axios";
import store from '../store'

const withTokenAxios = axios.create({
  baseURL: import.meta.env.VITE_APP_API,
  timeout: 5000,
});

withTokenAxios.interceptors.request.use(async function (config) {
  const isLogin = store.getters['session/isLogin'];
  console.log('isLogn', isLogin)
  if(isLogin){
    store.dispatch('session/checkTokenExpDate');
    // var isAccessTokenExpire = store.getters['session/isAccessTokenExpired'];
   }
  if (isLogin) {
    const access_token  = store.getters['session/getAccessToken'];
      try {
        config.headers['Authorization'] = `Bearer ${access_token}`
      } catch (err) {
        alert("Please log in again.\n" + err.response.data.errormessage);
      }
  }
  return config;
}, function (error) { 
  return Promise.reject(error);
});


withTokenAxios.interceptors.response.use(
    (response) => response,
    async (error) => {
      console.log("axios response error:", error)
  
      store.dispatch('session/checkTokenExpDate');
      // var isAccessTokenExpire = store.getters['session/isAccessTokenExpired'];
     
      const originalRequest = error.config;
      const refresh_token  = store.getters['session/getRefreshToken'];
      // Retry the request if it failed due to an expired token
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
  
        try {
          // Fetch a new access token using the refresh token
          const response = await axios.post('/api/member/token/refresh/', {
            refresh: refresh_token,
          });
         
          if (response.data.code =='token_not_valid'){
            store.dispatch('session/logoutSession');
            // router.push('/login');
            window.location.href = '/todologin';
          }else{
            axios.defaults.headers.common.Authorization = `Bearer ${response.data.access}`
            originalRequest.headers.Authorization = `Bearer ${response.data.access}` 
            let token_data = {
                access: response.data.access,
                refresh: refresh_token,
                
            };
            console.log("interceptors refresh token_data", token_data);
            store.dispatch("session/setToken", token_data);
            store.dispatch('session/getToken');
            return axios(originalRequest);
          }
          
        } catch (refreshError) {
          store.dispatch('session/logoutSession');
          window.location.href = '/todologin';
          return Promise.reject(refreshError);
        }
      }
    })

export default withTokenAxios
