<template>
    <div id="root">

<el-container>
  <el-aside width="200px">
          <Menu></Menu>
    </el-aside>
        <el-main>
<template>
<el-row>
 <el-col :span="12">
<el-input v-model="keyword"  placeholder="请输入您要查询的关键词">

<i slot="suffix" class="el-input__icon el-icon-search"></i>

 </el-input>
</el-col>
<el-col :span="12">
<el-input v-model="province"  placeholder="请输入您要查询的省份">

<i slot="suffix" class="el-input__icon el-icon-search"></i>

 </el-input>
</el-col>
</el-row>
<br>
<br>

 <el-button type="primary" @click="init">一键搜索</el-button>
  <light-timeline :items='items'></light-timeline>
</template>


            </el-main>
</el-container>
    </div>
    
    
</template>

<script>
//import {MapCtl, loadPolygon} from "../js/map";
//import {Provinces} from "../js/region";
//import * as maptalks from 'maptalks';
//import {loadBuilding} from "../js/building";
//import {loadLines3D} from "../js/lines3D";
import { Utils } from '../js/utils';
import {API} from "../js/server";
import Menu from './Menu.vue'

 

export default {
    name: 'News',
        components: {Menu},
    data () {

    return {
      keyword:'',
      province:'',
    search:'',
    raw:[],
      items: [ ]
};
    },
    mounted () {
this.init();
this.det();

    },
    methods: {
        btn(){},
        init () {

 let $this = this;
          let key = API.GetNews;
            Utils.ajaxData(key, {'keyword':this.keyword,'province':this.province}, function (rst) {
let i =0;
	$this.items=rst.data;
for (i=0;i<rst.data.length;i++){
$this.items[i]['tag']=rst.data[i]['pubDate'];
$this.items[i]['content']=rst.data[i].title + rst.data[i]['summary'];
}


            });
        },
det(){

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
.content{color:#051127;width:190px;height:80px;background-color:#0c2c45;border:1px solid #0c2c45}
.pop_title{float:left;padding-left:10px;width:180px;height:36px;line-height:36px;background:url(../assets/title.png);font-weight:bold;font-size:24px}
.pop_dept{float:left;padding:12px 5px;line-height:15px;text-align:center;margin:0 10px}
.pop_arrow{float:left;width:15px;height:24px;line-height:24px;background:url(../assets/arrow.png) no-repeat center center}
.arrow{display:block;width:17px;height:10px;background:url(../assets/em.png) no-repeat;position:absolute;left:50%;margin-left:-5px;bottom:-10px}
</style>