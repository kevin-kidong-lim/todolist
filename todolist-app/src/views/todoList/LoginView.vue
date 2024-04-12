<template>
    <div class="container">
  
      <div class="wrap-login100 input-form col-md-12 mt-2 mx-auto">
        <div class="w-100 d-flex justify-content-center pb-1">
          <span class="login100-form-title"> Todo List Login </span>
        </div>
        <loadingSpinner :mode="isLoading" />
        <div class="w-100 p-1 mt-5 d-flex justify-content-center pb-4">
          <!-- <form style="width: 22rem;"> -->
          <form id="login_form" style="width: 22rem" @submit.prevent="submitLogin">
            <!-- Email input -->
  
            <div class="form-outline mb-4 myname-form-input myname-form-input--floating" :class="state.user_id != '' ? 'myname-form-input--floating-top' : ''
              ">
              <input type="text" id="user_id" :value="state.user_id" @keyup="NumbersEngOnly"
                class="form-control form__input myname-form-input myname-form-input--floating" maxlength="12" />
              <!-- <label class="myname-label myname-label--floating" style="opacity: 1">ID</label> -->
              <label class="form-label" for="user_id" style="margin-left: 0px">ID</label>
              <small class="myname-label myname-label--secondary text-danger font-weight-bold small"
                v-if="v$.user_id.$error">{{ v$.user_id.$errors[0].$message }}</small>
            </div>
  
  
            <div class="form-outline mb-4 myname-form-input myname-form-input--floating"
              :class="state.password != '' ? 'myname-form-input--floating-top' : ''">
              <input type="password" id="password" v-model="state.password" class="form-control" />
              <label class="form-label" for="password" style="margin-left: 0px">Password</label>
              <small class="myname-label myname-label--secondary text-danger font-weight-bold small"
                v-if="v$.password.$error">{{ v$.password.$errors[0].$message }}</small>
            </div>
  
            <div class="row mb-4">
              
            </div>
  
            <!-- Submit button -->
            <button type="submit" class="btn-normal btn-login btn-block mb-4">
              Login
            </button>
  
            <!-- Register buttons -->
            <div class="text-center">
              <p><a href="#"  @click.prevent="goAggrement">Join</a></p>
              <p></p>
            </div>
  
          </form>
        </div>
      </div>
    </div>
  </template>
  <script>
  /* eslint-disable */
  
  import useValidate from "@vuelidate/core";
  import { useVuelidate } from "@vuelidate/core";
  import {
    required,
    helpers,
    email,
    sameAs,
    minLength,
  } from "@vuelidate/validators";
  import axios from "axios";
  import { userLogin } from '@/api/index';
  import { showAlert } from '@/utils/common.js';
  import { useStore } from "vuex";
  import { ref } from "vue";
  import { reactive, computed, onMounted, onUpdated, onBeforeUnmount } from "vue";
  import loadingSpinner from "@/components/LoadingSpinner.vue";
  import { useStorage } from "vue3-storage";
  
  import {
    useRouter,
  } from "vue-router";
  
  export default {
    components: {
      loadingSpinner
    },
    setup() {
      // const {sideBarInc} = sideBar()
      const store = useStore();
      const router = useRouter();
      const err_mesgs = ref([]);
      const storage = useStorage();
      const isLoading = ref(false);
      const showModal = ref(false)
      const site_name = ref('')
      const progress = ref(0)
      const state = reactive({
        user_id: "",
        password: "",
      });
      const rules = {
        user_id: { required: helpers.withMessage("* Required field", required) },
        password: {
          required: helpers.withMessage("* Required field", required),
          minLength: helpers.withMessage("at least 8 characters", minLength(8)),
        },
      };
  
      const v$ = useVuelidate(rules, state);
  
      const submitLogin = async function () {
        this.v$.$validate(); // checks all inputs
        if (!this.v$.$error) {
          const userData = {
            user_id: state.user_id,
            password: state.password,
           }

            await userLogin(userData)
            .then((response) => {
              window.sessionStorage.setItem("id", response.data.user_id); 
              sessionStorage.setItem("id222", response.data);
              let token_data = {
                access: response.data.access,
                refresh: response.data.refresh,
              };
              store.dispatch("session/setToken", token_data);
              err_mesgs.value = "";
  
              if (response.data.user_id != "") {
                const session_data = {
                  token: response.data.access,
                  userId: response.data.user_id,
                  user_type: response.data.user_flag,
                };
                store.dispatch("session/loginSession", session_data);
                storage.setStorageSync("s_user_id", state.user_id);
                const now_dt = ref(new Date());

                router.push({ name: "todolist", params: {} });
              } else {
                showAlert("We couldn't find an account associated with that email address. Please try again or create a new account.", "Close")
              }
            })
            .catch((err) => {
            
              if (err.response.data.message.indexOf("Network Error") > -1) {
                showAlert("The server is currently unavailable. Please try again later.", "Close")
               
              }
  
              if (err.response.data.message.indexOf("user_id or password is incorrect!") > -1) {
                showAlert("Your Id or Passwords do not match. Please re-enter your password.", "Close")
              }
  
            });
  
        } else {
          showAlert("Make sure all required fields are filled in.", "Close")
        }
      };
  
      const findPasword = () => {
        router.push({ name: "findPassword", params: {} });
      };
  
      const goAggrement = () => {
        router.push({ name: "register", params: {} });
      }
      const NumbersEngOnly = (e) => {
        if (e.target.id === "user_id") {
          state.user_id = e.target.value;
          return (state.user_id = state.user_id.replace(/[^a-zA-Z0-9]/g, ""));
        }
      };
  
      onMounted(() => {
        isLoading.value = false;
        const currentRouteName = router.currentRoute.value.name;
        if (currentRouteName == "logout") {
          store.dispatch("session/logoutSession");
        }
      });

      return {
        state,
        v$,
        err_mesgs,
        submitLogin,
        NumbersEngOnly,
        findPasword,
        goAggrement,
        isLoading,
        showModal,
        site_name,
        progress
      };
    },
  
  };
  </script>
  <style scoped>
  #content {
    width: 100%;
  }
  
  .input-form {
    max-width: 680px;
  
    margin-top: 80px;
    padding: 32px;
  
    background: #fff;
    -webkit-border-radius: 10px;
    -moz-border-radius: 10px;
    border-radius: 10px;
    -webkit-box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.15);
    -moz-box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.15);
    box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.15);
  }
  
  .wrap-login100 {
    width: 500px;
    background: #fff;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 3px 20px 0 rgba(0, 0, 0, 0.1);
    -moz-box-shadow: 0 3px 20px 0 rgba(0, 0, 0, 0.1);
    -webkit-box-shadow: 0 3px 20px 0 rgba(0, 0, 0, 0.1);
    -o-box-shadow: 0 3px 20px 0 rgba(0, 0, 0, 0.1);
    -ms-box-shadow: 0 3px 20px 0 rgba(0, 0, 0, 0.1);
  }
  
  .login100-form-title {
    /* font-family: JosefinSans-Bold; */
    font-size: 20px;
    color: #fff;
    line-height: 0.4;
    text-align: center;
    display: block;
    position: absolute;
    width: 100%;
    top: 0;
    left: 0;
    background-color: #33465c;
    /* background-color: #57b846; */
    padding-top: 25px;
    padding-bottom: 30px;
  }
  
  .wrap-input100 {
    width: 100%;
    background-color: #fff;
    border-radius: 27px;
    position: relative;
    z-index: 1;
  }
  
  .m-b-16 {
    margin-bottom: 16px;
  }
  
  .btn-login {
    color: #fff;
    background-color: #33465c;
    border-color: #33465c;
  }
  
  .btn-login:hover {
    background-color: #26374a;
    transition: 0.7s;
    border: 1px solid #ffbf00;
    /* border-radius: 20px; */
  }
  
  
  .modal {
    display: none;
    /* align-items: center;
    justify-content: center; */
    position: fixed;
    z-index: 1050;
    /* top: 200px;
    left: 200px; */
    top: 40%;
    left: 40%;
    transform: translate(-40%, -40%);
    /* width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    outline: 0; */
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .modal.show {
    display: block;
  }
  
  .modal-dialog {
    /* position: relative;
    width: auto;
    margin: 10px; */
  
    position: absolute;
    top: 40%;
    left: 30%;
    transform: translate(-40%, -30%);
    min-width: 600px;
    max-width: 800px;
  
  }
  
  .modal-content {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    pointer-events: auto;
    background-color: #fff;
    background-clip: padding-box;
    border: 1px solid rgba(0, 0, 0, 0.2);
    border-radius: 0.3rem;
    outline: 0;
  }
  
  .modal-body p{
    color: #33465c;
    font-size: 0.9rem;
    /* font-weight: 600; */
  }
  </style>
  