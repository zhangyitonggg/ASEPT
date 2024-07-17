<template>
<el-row class="demo-avatar demo-basic">
    <el-col :span="12">
      <!-- <div class="sub-title">circle</div> -->
      <div class="demo-basic--circle">
        <div class="block"><el-avatar :size="150" :src="circleUrl"></el-avatar></div>
        
      </div>
    </el-col>  
    
  </el-row>
    
</template>

<script>
    export default {
        name:"Avatar",
        data () {
             return {
                circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
            }
        },
    }

</script>

<style>


</style>