// import jwtDecode from 'jwt-decode';
import { jwtDecode } from "jwt-decode";
// initial state
/* eslint-disable */
const state = {
    userId: null,
    token: '',
    // userid: '',
    user_type: 0,
    access_token: '',
    refresh_token:'',
    access_token_exp:'',
    today_: new Date()
  };
  
  // getter
  const getters  = {
    isLogin(state){
      if ( state.userId  == '' || state.userId  == null){
        return false;
      }else{
        return true;
      }
    },
    getLogin(state) {
      return typeof state.token === 'string' && state.token !== ''
    },
    getToken(state) {
      return state.token
    },
    getUserId(state) {
      console.log('getUserId from session:')
      return state.userId
    },
    getUserType(state) {
      return state.user_type
    },
    getAccessToken(state){
      return state.access_token
    },
    getRefreshToken(state){
      return state.refresh_token
    },
    isAccessTokenExpired(state){
      // Check if the accessToken exists and if its expiration time has passed
     console.log('######### start1 #########')
      
      if ( state.access_token_exp != '') {
        const expirationDate = new Date(state.access_token_exp * 1000); 
      
        if ( expirationDate > state.today_ ) {
          return false;
        }else{
          return true;
        }
      }else{
        return true;  
      }

    },
    
  };
  
  // mutations
  const mutations = {
    chgUserId(state, newId) {
      state.userId = newId;
    },
    setSession(state, n) {
      
      state.token = n.token
      state.userId = n.userId
      state.user_type = n.user_type
    },
    logoutSession(state) {
      sessionStorage.clear()
      state.token = ''
      state.userId = ''
      state.user_type = 0
      state.access_token = ''
      state.refresh_token = ''
    },
    setToken(state, n) {
     
      state.access_token = n.access
      state.refresh_token = n.refresh
      const decoded  = jwtDecode(state.access_token)
      state.access_token_exp = decoded.exp
      
    },
    checkTokenExpDate(state, n){
      state.today_ = new Date()
    }
  };
  
  // Actions
  const actions = {
    callMutation({commit, state}, newId) {
      sessionStorage.setItem('id', newId)
      commit('chgUserId', newId);
    },
    loginSession(context, data) {
     
      sessionStorage.setItem('session', JSON.stringify(data))
      context.commit('setSession', data)
    },
    setToken(context, data) {
    
      sessionStorage.setItem('token', JSON.stringify(data))
      context.commit('setToken', data)
    },
    getSession(context) {
    
      const session = sessionStorage.getItem('session')
     
      if (session && typeof session === 'string' && session !== '') {
        const data = JSON.parse(session)
        context.commit('setSession', data)
      }
    },
    getToken(context) {
     
      const session = sessionStorage.getItem('token')
     
      if (session && typeof session === 'string' && session !== '') {
        const data = JSON.parse(session)
        context.commit('setToken', data)
      }
    },
    checkTokenExpDate(context){
      context.commit('checkTokenExpDate')
    },
    logoutSession(context) {
    
      context.commit('logoutSession')
    }
  };
  
  export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
  };

