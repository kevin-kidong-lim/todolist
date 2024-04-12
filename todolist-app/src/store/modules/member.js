  const state = {
    userId: null,
    token: '',
    // userid: '',
    user_type: 0,
    access_token: '',
    refresh_token:'',
  };
  // getter
  const getters  = {
    doneTodos (state) {
      return state.user_type
    }
  }

  
  export default {
    namespaced: true,
    state,
    getters ,
  };
