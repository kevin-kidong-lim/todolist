
import Vuex from 'vuex';
import 'es6-promise/auto';
import session from './modules/session';
import member from './modules/member';

/* eslint-disable */
export default new Vuex.Store({
  modules: {
    session,member
  },
});