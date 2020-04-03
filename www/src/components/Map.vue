<template>
    <div id="root">


<template>
<input type="text" name ="" id="" placeholder="输入您要鉴别的舆论" v-model="search"/>
<button @click="btn">搜索</button>
  <light-timeline :items='items'></light-timeline>
</template>

        <div style="position: fixed; right: 10px; top: 90px; font-weight: 400; font-family: 宋体;  " class="blink">
          

<router-link to="/china">返回</router-link>
        </div>
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

 

export default {
    name: 'Map',
    data () {

    return {
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
          let key = API.GetRumors;
            Utils.ajaxData(key, {'need':'none'}, function (rst) {
let i =0;
	$this.items=rst.data;
for (i=0;i<rst.data.length;i++){
$this.items[i]['tag']='2020年3月20日';
$this.items[i]['content']=rst.data[i].title + rst.data[i]['mainSummary'];
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
#root {
    height: calc(100% - 115px); 
}
a{color: #dd4814}
.el-input__inner { color: #fff; background-color: #0c2c45}
.content{color:#fff;width:190px;height:80px;background-color:#051127;border:1px solid #0c2c45}
.pop_title{float:left;padding-left:10px;width:180px;height:36px;line-height:36px;background:url(../assets/title.png);font-weight:bold;font-size:16px}
.pop_dept{float:left;padding:12px 5px;line-height:15px;text-align:center;margin:0 10px}
.pop_arrow{float:left;width:15px;height:24px;line-height:24px;background:url(../assets/arrow.png) no-repeat center center}
.arrow{display:block;width:17px;height:10px;background:url(../assets/em.png) no-repeat;position:absolute;left:50%;margin-left:-5px;bottom:-10px}
</style>