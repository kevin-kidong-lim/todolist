<template>
  <div class="container-fluid">
    <!-- Sidebar  justify-content-center -->
    <div class="container ml-2">
      <div class="row">
        <div class="col-3" v-if="mode == 'update'">
        </div>
        <div class="col-2" v-else>
        </div>
        <div class="col-8">
          <div class="container">
            <h3>{{ title }} </h3>
            <hr>
            <!-- Page Content -->
            <div id="content" v-if="routeName == 'update'">
              <memberRegister mode='update' />
            </div>
            <div id="content" v-else-if="routeName == 'register'">
              <memberRegister mode='create' />
            </div>
          </div>
        </div>
        <div class="col-1">
        </div>
      </div>
    </div>
  </div>
</template>
<script>
/* eslint-disable */
// @ is an alias to /src
import memberRegister from '@/components/member/MemberRegister.vue'

import { ref, onMounted } from 'vue'
import {useRouter,} from "vue-router";

export default {
  name: 'RegisterView',
  components: {
    memberRegister,
  },
  setup() {
    const router = useRouter()
    const mode = ref('')
    const title = ref('')
    const routeName = ref('')

    onMounted(() => {
      const currentRouteName = router.currentRoute.value.name
      routeName.value = currentRouteName
      if (currentRouteName == 'update') {
        mode.value = "update"
        title.value = 'Profile'
      } else {
        mode.value = "create"
        title.value = 'Profile'
      }
    })

    return {
      mode,
      title,
      routeName
    }
  }
}
</script>
<style>
.wrapper {
  display: flex;
  align-items: stretch;
}

#sidebar {
  min-width: 250px;
  max-width: 250px;
}

#sidebar.active {
  margin-left: -250px;
}

#content {
  width: 100%
}
</style>