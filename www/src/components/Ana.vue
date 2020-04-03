<template>
    <div id="root">
<el-container>
  <el-aside width="200px">
          <Menu></Menu>
    </el-aside>
        <el-main>
<img src="../assets/detc.png"  style="width:500px; height:80px">
<br>
<el-input v-model="input" 
rows="15"  placeholder="请输入您要判断的言论">

<i slot="suffix" class="el-input__icon el-icon-search"></i>

 </el-input>
<br>
<br>

 <el-button type="primary" @click="Search">一键搜索</el-button>
 <br>
<br>
        <br>
        <br>
        <el-input v-model="output" rows="15" placeholder="请搜索后等待反馈" :disabled="true" ></el-input>
            </el-main>
</el-container>
    </div>
    
    
</template>

<script>

import Menu from './Menu.vue'

 

export default {
    name: 'Ana',
        components: {Menu},
    data () {

    return {
      Img: 'assets/detc.png',
input:'',
output:'暂时没有输出呢'
};
    },
    mounted () {

    },
    methods: {
Search(){

}
    }
}
</script>
<style>
.pageHead {
  height: 100px !important; 
  padding-top: 5px !important;
  padding-bottom: 10px !important;
}
.f{
  color:black
}
#root {
    height: calc(100% - 115px); 
}
a{color: #dd4814}
.el-input__inner { color: #fff; background-color: #0c2c45}
.content{color:#051127;width:190px;height:80px;background-color:#0c2c45;border:1px solid #051127}
.pop_title{float:left;padding-left:10px;width:180px;height:36px;line-height:36px;background:url(../assets/title.png);font-weight:bold;font-size:16px}
.pop_dept{float:left;padding:12px 5px;line-height:15px;text-align:center;margin:0 10px}
.pop_arrow{float:left;width:15px;height:24px;line-height:24px;background:url(../assets/arrow.png) no-repeat center center}
.arrow{display:block;width:17px;height:10px;background:url(../assets/em.png) no-repeat;position:absolute;left:50%;margin-left:-5px;bottom:-10px}
</style>