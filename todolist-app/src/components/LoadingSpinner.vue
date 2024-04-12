
<template>
    <div class="container">
        <div class="loader d-flex justify-content-center">
            <div>
            <easy-spinner v-show="isLoading"
            :type="spinerState.type" 
            :color="spinerState.color" 
            :size="spinerState.size" 
            ></easy-spinner>
            </div>
        </div>
</div>
</template>
<script>

import { reactive,onMounted,ref,onUpdated} from 'vue'
export default {
  name: "LoadingSpinner",
  props: ["mode"],
  setup(props){
    
       let spinerState = reactive({
            color: '#fb8500',
            size: 60,
            type: 'spins',  // spins\circular\dots	
            });
        const isLoading = ref(true)
        onMounted(() => {
            isLoading.value = props.mode
     
        })
        onUpdated( () => {
            isLoading.value = props.mode
     
        })
     
     return {
        spinerState,
        isLoading
          
     }
  }
  
};
</script>