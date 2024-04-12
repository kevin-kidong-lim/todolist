<template>
  <div class="container">
    <div class="input-form-backgroud row">
      <div class="col-md-12 d-flex justify-content-between align-items-center">
        <h1 class="d-inline-block mb-0">Todo List</h1>
        <div class="mb-3 mt-3" style="display: flex; align-items: center;">
          <div class="user-initials" style="margin-right: 10px;">
            {{ getUserInitials(session_user_id) }}
          </div>
          <div>
            <a @click="updateProfile()">{{ session_user_id }}<i class="bi bi-pencil-square ml-1 mr-1"
                style="font-size: 23px; color: red;"></i></a>
            <a @click="logout()" class="btn btn-outline-secondary btn-sm">Logout</a>
          </div>
        </div>
      </div>
    </div>
    <div class="input-form-backgroud row mt-3">
      <div class="input-form col-md-12 mx-auto">
        <form @submit.prevent="submitForm">
          <div id="newtask">
            <div class="d-flex align-items-center">
              <input type="text" v-model="todoData.title" id="title" placeholder="Add Tasks" class="mr-2">
              <button class="btn btn-primary" v-if="todoData.mode === 'create'">Add</button>
              <button class="btn btn-primary" v-if="todoData.mode === 'update'">Update</button>
              <a @click="resetAddForm()"><i class="bi bi-file-excel-fill ml-2" style="font-size: 33px; color: red;"
                  v-if="todoData.mode === 'update'"></i></a>
            </div>
          </div>
        </form>
        <div class="task-filter">
          <button type="button" @click="setProgress('all')" 
            class="btn btn-outline-secondary  mr-1" 
            :class="{ active: todoData.progress === 'all' }"
            id="all-btn">All</button>
          <button type="button" @click="setProgress('inprogress')" 
            class="btn btn-outline-secondary mr-1" 
            :class="{ active: todoData.progress === 'inprogress' }"
            id="in-progress-btn">In Progress</button>
          <button type="button" @click="setProgress('completed')" 
            class="btn btn-outline-secondary mr-1" 
            :class="{ active: todoData.progress === 'completed' }"
            id="completed-btn">Completed</button>
        </div>
        <div id="tasks">
          <div class="list-item" v-for="item in dataList" :key="item.id">
            <input type="checkbox" :id="`checkbox-${item.id}`" @click="toggleCompleted(item.id)"  :checked="item.completed">
            <h5 style="width: 80%"> 
              <a  @click="completedUpdate(item.id, item.completed)">
                <span  :class="{ 'completed-line': item.completed }">{{item.title }}</span>
              </a>
              <span class="completed-status" v-if="item.completed"> / Completed: {{ formatDate(item.completed_at) }}</span>
             </h5>
            <div class="item-info">
              <div class="buttons">
                <button class="btn btn-sm btn-info" @click="setTodoUpdate(item.id, item.title)">Update</button>
                <button class="btn btn-sm btn-danger" @click="todoDelete(item.id)">Delete</button>
              </div>
              <p class="date" v-if="item.completed">{{ formatDate(item.completed_at) }} </p>
              <p class="date" v-else>{{ formatDate(item.created_at) }} </p>
            </div>
          </div>
        </div>
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
import axios from "axios";
import { getRequestWithAuthApi, postRequestWithAuthApi, putRequestWithAuthApi, deleteRequestWithAuthApi } from '@/api/index';
import { showAlert, formatDate } from '@/utils/common.js';
import { useStore } from "vuex";
import { ref } from "vue";
import { reactive, computed, onMounted, onUpdated, onBeforeUnmount } from "vue";
import loadingSpinner from "@/components/LoadingSpinner.vue";
import { useStorage } from "vue3-storage";
import jQuery from "jquery";
import {
  useRouter, useRoute
} from "vue-router";

export default {
  components: {
    loadingSpinner
  },
  setup() {
    // const {sideBarInc} = sideBar()
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    const err_mesgs = ref([]);
    const storage = useStorage();
    const isLoading = ref(false);
    const showModal = ref(false)
    const site_name = ref('')
    const progress = ref(0)
    const session_user_id = ref(null)
    const dataList = ref([])

    const todoData = reactive({
      title: '',
      content: '',
      id: '',
      complete: '',
      progress: 'all',
      mode: 'update'
    })
    const rules = {
      title: { required: helpers.withMessage('* Required field.', required) },
    };

    const v$ = useVuelidate(rules, todoData);

    const submitForm = async function () {
      this.v$.$validate() // checks all inputs
      if (!this.v$.$error) {
        if (todoData.mode == 'create') {
          const payload = {
            user_id: store.state.session.userId,
            title: todoData.title
          }
          await postRequestWithAuthApi('/api/todolist/', payload)
            .catch(error => {
              showAlert("The server is currently unavailable. Please try again later.", "닫기")
            });
          getData()
          resetAddForm()
        } else {

          const payload = {
            user_id: store.state.session.userId,
            title: todoData.title,
            id: todoData.id
          }
          await putRequestWithAuthApi('/api/todolist/' + todoData.id + '', payload)
            .catch(error => {
              showAlert("The server is currently unavailable. Please try again later.", "Close")
            });
          getData()
        }
      } else {
        showAlert("Please check your input and make sure all fields are filled in correctly.", "Close")
      }
    }


    const getUserInitials = (username) => {
      let initials = null
      if (username != null)
        initials = username.split(' ').map(name => name.charAt(0).toUpperCase()).join('')
      return initials;
    }
    const logout = () => {
      store.dispatch('session/logoutSession');

      router.push({
        name: 'todologin', params: {
        }
      })
    }

    const updateProfile = () => {
      router.push({ name: "update", params: {} });
    }

    const setProgress = (progress) => {
      todoData.progress = progress
      getData()
    }
    const getData = async () => {
      isLoading.value = true

      const session_user_id = store.state.session.userId
      const params = {
        user_id: session_user_id,
        progress: todoData.progress,
        page_size: 5,
        notice_flag: 123
      }

      await getRequestWithAuthApi('/api/todolist/list/' + session_user_id + '', params)
        .then((res) => {
          isLoading.value = false
          dataList.value = res.data
        }).catch((err) => {
          isLoading.value = false
          showAlert("The server is currently unavailable. Please try again later.", "Close")
        })
    }
    const toggleCompleted = (id) => {
      const item = dataList.value.find(item => item.id === id);
      completedUpdate(id, item.completed)
      // item.completed = !item.completed;
      

    }
    const completedUpdate = async (id, completed) => {
      const payload = {
        completed: !completed
      }
      await putRequestWithAuthApi('/api/todolist/detail/' + id + '', payload)
        .catch(error => {
          showAlert("The server is currently unavailable. Please try again later.", "Close")
        });
      getData()
      resetAddForm()
      // 추가 코드: `title` 클릭 시 `checkbox` 체크 및 애니메이션 효과
      const checkbox = document.getElementById(`checkbox-${id}`);
      checkbox.checked = !completed;
      checkbox.classList.add('animated', 'bounce');
      setTimeout(() => {
        checkbox.classList.remove('animated', 'bounce');
      }, 1000);
    }
    const todoDelete = async (id) => {
      const payload = {
        id: id
      }
      await deleteRequestWithAuthApi('/api/todolist/' + id + '', payload)
        .catch(error => {
          showAlert("The server is currently unavailable. Please try again later.", "Close")
        });
      getData()
      resetAddForm()
    }


    const setTodoUpdate = (id, title) => {

      todoData.title = title
      todoData.id = id
      todoData.mode = 'update'
      let s_top = jQuery("#newtask").offset().top;
      jQuery("html,body").animate({ scrollTop: s_top + 5 }, "slow");
    }

    const resetAddForm = () => {
      todoData.title = ''
      todoData.id = ''
      todoData.mode = 'create'
    }
    const todoUpdate = async (id, title) => {
      const payload = {
        title: title
      }
      await putRequestWithAuthApi('/api/todolist/detail/' + id + '', payload)
        .catch(error => {
          showAlert("The server is currently unavailable. Please try again later.", "Close")
        });
      getData()
    }



    onMounted(() => {
      isLoading.value = false;
      const currentRouteName = router.currentRoute.value.name;
      if (currentRouteName == "logout") {
        store.dispatch("session/logoutSession");
      }
      session_user_id.value = store.state.session.userId

      if (route.params.id === undefined) {
        todoData.mode = 'create'
      } else {
        todoData.mode = 'update'
        todoData.id = route.params.id

      }
      getData()
    });


    return {
      setProgress,
      toggleCompleted,
      todoDelete,
      resetAddForm,
      v$,
      err_mesgs,
      setTodoUpdate,
      todoUpdate,
      formatDate,
      submitForm,
      completedUpdate,
      isLoading,
      showModal,
      site_name,
      progress,
      getUserInitials,
      logout,
      session_user_id,
      todoData,
      getData,
      dataList,
      updateProfile
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
  box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.15)
}
</style>