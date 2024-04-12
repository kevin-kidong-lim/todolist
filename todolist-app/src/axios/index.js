
import axios from 'axios'
import store from '../store'
// import router from '../router'

const withTokenAxios = axios.create({
  baseURL: import.meta.env.VITE_APP_API,
  timeout: 5000,
});

withTokenAxios.interceptors.request.use(async function (config) {

  const isLogin = store.getters['session/isLogin'];
  if(isLogin){
    store.dispatch('session/checkTokenExpDate');
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
  // Handle request errors
  return Promise.reject(error);
});


withTokenAxios.interceptors.response.use(
    (response) => response,
    async (error) => {
      store.dispatch('session/checkTokenExpDate');
  
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
            // console.log('refreshError: token_not_valid')
            store.dispatch('session/logoutSession');
            // router.push('/login');
            window.location.href = '/todologin';
          }else{
            axios.defaults.headers.common.Authorization = `Bearer ${response.data.access}`
            originalRequest.headers.Authorization = `Bearer ${response.data.access}` 
            // Update the stored access token
            // setAccessToken(response.data.access);
            let token_data = {
                access: response.data.access,
                refresh: refresh_token,
                
            };
    
            // console.log("interceptors refresh token_data", token_data);
            store.dispatch("session/setToken", token_data);
            store.dispatch('session/getToken');
    
            // Retry the original request with the new access token
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