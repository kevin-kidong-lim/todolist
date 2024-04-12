<template>
  <div class="container">
    <div class="input-form-backgroud row">
        <div class="input-form col-md-12 mx-auto">
        <form @submit.prevent="submitForm">
          <div class="row">
            <div class="col-md-6 mb-3 mt-3 myname-form-input myname-form-input--floating" 
              :class="state.user_id != null || state.user_id != '' ? 'myname-form-input--floating-top' : ''"
               v-if=" mode == 'update' ">
                <!-- <label for="user_id" class="form-label">ID</label>  -->
                <input type="text" class="form-control" id="user_id"
                v-model="state.user_id"
                 placeholder="ID"  readonly>
                 <label class="myname-label myname-label--floating ml-2" style="opacity: 1;"> ID</label>
              </div>
           
            <div class="col-md-6 mb-3 mt-3 myname-form-input myname-form-input--floating" 
                :class="state.user_id != null ? 'myname-form-input--floating-top' : ''"
                v-else>
                  <input type="text" 
                  class="form-control form__input myname-form-input myname-form-input--floating"
                  id="user_id"
                  v-model ="state.user_id" 
                   @keyup="NumbersEngOnly"
                   placeholder="" maxlength="12" >
                   <label class="myname-label myname-label--floating ml-2"  for="user_id" style="opacity: 1;"> ID</label>
                                  <label class="myname-label myname-label--secondary text-danger font-weight-bold small" 
                                  for="user_id" v-if="v$.user_id.$error">{{ v$.user_id.$errors[0].$message }}</label>
                </div>
            <div class="col-md-6 mb-3 mt-3  myname-form-input myname-form-input--floating" 
              :class="state.user_nm != '' ? 'myname-form-input--floating-top' : ''">
                <!-- <label for="user_nm">이름</label> -->
                <input type="text"
                class="form-control form__input myname-form-input myname-form-input--floating"
                 id="user_nm" 
                 placeholder=""
                 v-model="state.user_nm" 
                  @keyup="NumbersEngHanOnly"
                   maxlength="12" >
                   <label class="form-label" for="user_nm" style="margin-left: 0px">Name</label>
                <label class="myname-label myname-label--secondary text-danger font-weight-bold small" 
                for="user_nm"  v-if="v$.user_nm.$error">{{ v$.user_nm.$errors[0].$message }}</label>
              </div>


          </div>

            <div class="row"   v-if="mode == 'create' ">
              <div class="col-md-6 mb-3  myname-form-input myname-form-input--floating" 
              :class="state.password != '' ? 'myname-form-input--floating-top' : ''">
                <input type="password" 
                class="form-control form__input myname-form-input myname-form-input--floating"
                id="password"
                 v-model="state.password" 
                 placeholder=""   
                 maxlength="20" >
                 <label class="myname-label myname-label--floating ml-2"  for="password"  style="opacity: 1;"> Password</label>
                <label class="myname-label myname-label--secondary text-danger font-weight-bold small" 
                for="password"  v-if="v$.password.$error">{{ v$.password.$errors[0].$message }}</label>
             
              </div>

            <div class="col-md-6 mb-3  myname-form-input myname-form-input--floating" 
              :class="state.password2 != '' ? 'myname-form-input--floating-top' : ''">
                <!-- <label for="password2">비밀번호 확인</label> -->
                <input type="password" 
                class="form-control form__input myname-form-input myname-form-input--floating"
                id="password2"
                 v-model="state.password2" 
                  placeholder=""   
                  maxlength="20" >
                  <label class="myname-label myname-label--floating ml-2"   for="password2"  style="opacity: 1;"> Password Confirm</label>
                <label class="myname-label myname-label--secondary text-danger font-weight-bold small" 
                for="password2"   v-if="v$.password2.$error">{{ v$.password2.$errors[0].$message }}</label>

              </div>

          </div>
          <div class="mb-3 myname-form-input myname-form-input--floating" 
              :class="state.email != '' ? 'myname-form-input--floating-top' : ''">
              <!-- <label for="email">이메일</label> -->
              <input type="email" 
              class="form-control "
              id="email" 
               v-model="state.email" 
               placeholder=""   
               maxlength="100" >
               <label class="myname-label myname-label--floating ml-2"   for="email" style="opacity: 1;">you@example.com</label>
                <label class="myname-label myname-label--secondary text-danger font-weight-bold small" 
                for="email"  v-if="v$.email.$error">{{ v$.email.$errors[0].$message }}</label>
            </div>
           
          <!-- comp_no  comp_owner comp_file -->
      
          
          <div class="mb-3 text-center">
            <button
              class="btn btn-primary btn-lg col-lg-2"
              v-if="mode == 'update'"
            >
              Update
            </button>
            <a @click="moveTodoList()"  class="btn btn-primary btn-lg col-lg-2 ml-2" v-if="mode == 'update'" >
              TodoList
            </a>
            <button class="btn btn-primary btn-lg col-lg-2" v-else>Create</button>
          </div>
          <!-- @click="submitForm()"  -->
        </form>

        <ul class="text-danger font-weight-bold small" v-if="err_mesgs">
          <li v-for="(item, index) in err_mesgs" :key="index">
            {{ item }} / {{ index }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import { useVuelidate } from "@vuelidate/core";
import {
  required,
  helpers,
  email,
  sameAs,
  minLength,
} from "@vuelidate/validators";
import { showAlert,NumbersEngHanOnly,NumbersOnly,NumbersEngOnly,showAlertWithIcon,ICON_TYPES } from '@/utils/common.js';
import { putMultipartRequestWithAuthApi,getRequestWithAuthApi, postMultipartRequestApi} from '@/api/index';
import { ref } from "vue";
import { useStore } from 'vuex'
import { reactive, onMounted } from "vue";
import { useRouter} from "vue-router";

export default {
  props: ["mode"],
  setup(props, { emit }) {
    const store = useStore();
    const router = useRouter();
    const err_mesgs = ref([]);
    const state = reactive({
      user_id: "",
      password: "",
      password2: "",
      user_nm: "",
    
      email: "",
     
      member_flag: "",
    });
    const passwordIsSame = (password) => {
      return password === state.password;
    };
    let rules = "";

    if (props.mode == "update") {
      rules = {
        user_nm: {
          required: helpers.withMessage("*  Required field.", required),
        },
     
        email: {
          email: helpers.withMessage("Please enter a valid email address.", email),
          required: helpers.withMessage("*  Required field", required),
        },
        
      };
    } else {
      rules = {
        user_id: {
          required: helpers.withMessage("*  Required field", required),
        },

        password: {
          required: helpers.withMessage("*  Required field", required),
        },
        password2: {
          required: helpers.withMessage("*  Required field", required),
          minLength: helpers.withMessage(
            "at least 8 characters long",
            minLength(8)
          ),
          sameAsPassword: helpers.withMessage(
            "It doesn't match.",
            passwordIsSame
          ),
        }, 

        user_nm: {
          required: helpers.withMessage("* Required field.", required),
        },
        name: "",
       
        email: {
          email: helpers.withMessage("Please enter a valid email address.", email),
          required: helpers.withMessage("* Required field", required),
        },
        
      };
    }

    const v$ = useVuelidate(rules, state);

    async function submitForm() {
      this.v$.$validate(); // checks all inputs
      if (!this.v$.$error) {
        if (props.mode == "update") {
          const formData = new FormData();
          formData.append("user_id", session_user_id.value);
          formData.append("user_nm", state.user_nm);
          formData.append("email", state.email);
            await putMultipartRequestWithAuthApi("/api/member/detail/" + session_user_id.value + "",formData )
            .then((response) => {
                getData();
              
            })
            .catch((err) => {
              
              if (err.message.indexOf("Network Error") > -1) {
                showAlert("The server is currently unavailable. Please try again later.", "닫기")
              }
            });
        } else {
          const formData = new FormData();
          formData.append("user_id", state.user_id);
          formData.append("user_nm", state.user_nm);
          formData.append("password", state.password);
          formData.append("password2", state.password2);
          formData.append("email", state.email);
            await postMultipartRequestApi("/api/member/register/",formData)
            .then((response) => {
              err_mesgs.value = "";
              showAlertWithIcon("Please log in.", ICON_TYPES.SUCCESS, true, "Login")
              .then( (result) => {
                  if (result.isConfirmed) {
                    router.push({ name: "login" });
                  }else{
                    router.push({ name: "main" });
                  }
              })
              
            })
            .catch((err) => {
              // err_mesgs.value.push(err.response.data)
              if (err.response.data.user_id != null) {
                showAlert("This id is already taken.", "Close")
                return;
              }
              if (err.response.data.email != null) {
                showAlert("This email is already taken.", "Close")
                return;
              }
             
              if (err.message.indexOf("Network Error") > -1) {
                showAlert("The server is currently unavailable. Please try again later.", "Close")
              }
            });
        }
      } else {
        showAlert("Please check your input and make sure all fields are filled in correctly.", "Close")
      }
    }
    const session_user_id = ref("");
    const getData = async () => {
      
        await getRequestWithAuthApi("/api/member/detail/" + session_user_id.value + "",'')
        .then((res) => {
          state.user_nm = res.data.user_nm;
          state.password = res.data.password;
          state.email = res.data.email;
          
        })
        .catch((err) => {
          showAlert("The server is currently unavailable. Please try again later.", "Close")
        });
    };

    const main_file = ref("");

    const selectMainFile = function (e) {
      main_file.value = e.target.files[0];
    };

    const moveTodoList = () => {
      router.push({ name: "todolist", params: {} });
    }
  

    const currentRouteName = router.currentRoute.value.name;
    onMounted(() => {
      
      session_user_id.value = store.state.session.userId;
      state.user_id = store.state.session.userId;
      state.member_flag = store.state.session.user_type;

      if (
        currentRouteName == "update"
      ) {
        getData();
      } 
    });

    return {
      state,
      v$,
      submitForm,
      err_mesgs,
      getData,
      session_user_id,
      selectMainFile,
      moveTodoList,
      main_file,
      NumbersOnly,
      NumbersEngOnly,
      NumbersEngHanOnly,
      currentRouteName,
    };
  },
};
</script>
<style scoped>
body {
  min-height: 100vh;
}

.input-form {
  /* max-width: 680px;
    margin-top: 80px;
    padding: 32px; */

  background: #fff;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  -webkit-box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.15);
  -moz-box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.15);
  box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.15);
}
</style>
