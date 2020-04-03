<template>
  <div>
    <div style="text-align: left; " class="pageHead">
      <div style="text-align: right; ">
        <span>
          <a href="https://github.com/ZhaohengLi/covid-19-visualization" style="color: #fff; text-decoration:none">
            <img style="margin-bottom: -2px;" src="../assets/github.png" width="18" /> 
            <label style="font-size: 16px"> Github</label>
          </a>
        </span>
      </div>
      <div>
        <div style="font-size: 24px">新冠肺炎疫情<label style="font-size: 22px"> · 数据分析系统</label></div>
        <div style="font-size: 20px; margin-top: 5px; color: #ddd; font-family: 'Times New Roman', Times, serif">
          COVID-19 Data Visualization Analysis System
        </div>

      </div>

    </div>
               <div class="hello">

        <div style="text-align: left">
            <div style="height: 40px; line-height: 40px">
                <label style="float: right; color: #4197FD">数据更新时间： {{updateTime}}</label>
            </div>
        </div>
        <!-- 总体数据汇总情况 -->
        <el-card class="box-card" style="background: #f4f5f9; ">
            <el-row :gutter="20">
                <el-col :span="6" v-for="item in sums" :key="item.name">
                    <div class="grid-content ">
                        <div class="sum_numb" :style="{color: item.color, fontSize: '20px', marginBottom: '8px'}">{{item.sum}}</div>
                        <div class="sum_numb" style="color: #333333; font-size: 14px">{{item.text}}病例</div>
                        <div class="sum_numb" style="font-size: 13px; color: #999999; margin-top: 8px">
                            <label style="font-weight:200">昨日 </label>
                            <label :style="{color: item.color}">{{item.add}}</label>
                        </div>
                    </div>
                </el-col>
            </el-row>
        </el-card>
    </div>

  </div>
</template>

<script>
import {Utils} from "../js/utils";
//import {API} from "../js/server";

export default {
  name: 'Head',

  
    data () {
        return {
            updateTime:'',
            sums:[],
            items:[{'tag':'1-2-3','content':'1-2-3'}],
            activeName: '',
            mapHeight: (Utils.getDevice() === 'xs') ? "330px" : "500px"
        }
    },

mounted(){

this.updateTime = this.$store.state.updateTime;
this.sums = this.$store.state.sums;
},

computed: {
listenstore(){
return this.$store.state.updateTime;
}
},

    watch: {
listenstore: function(){
this.updateTime = this.$store.state.updateTime;
this.sums = this.$store.state.sums;
},


methods: {

}
}
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0px;
}
a, a>label { cursor: pointer }
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
.pageHead {
  height: 160px; 
  padding: 20px;
  background: url(../assets/head.png) center top / 100% no-repeat;
  color: #fff
}

.el-main { 
  padding: 0px 15px 20px 15px!important;
  height: calc(100% - 200px);
  /* min-height: calc(100% - 200px); */
}
.el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px; 
}
.el-footer {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
}
.el-scrollbar__wrap{
    overflow-x: hidden!important;
}

</style>
