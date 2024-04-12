<template>
  <div id="app">
    <div>
      <loadingSpinner  :mode = isLoading />
      <router-view></router-view>
    </div>
  </div>

</template>

<script>

import { useRouter } from 'vue-router';
import { ref } from 'vue'
import loadingSpinner from '@/components/LoadingSpinner.vue'
// import {container} from "jenesius-vue-modal";
export default {
  components: {
    loadingSpinner,
  },
  setup() {
    const router = useRouter();
    const isLoading = ref(true);

    // Show loading spinner before navigating to a new route
    router.beforeEach((to, from, next) => {
      isLoading.value = true;
      next();
    });

    // Hide loading spinner after navigation completes
    router.afterEach(() => {
      isLoading.value = false;
    });

    return {
      isLoading
    };
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}

</style>
