<template>
  <div class="hello">
    <el-main>
        <Common :title="loader.title" :updateTime="loader.updateTime" :sums="loader.sums" :tabs="tabs" :activeName_="loader.activeName"
        @handleClickTab="click($event)" />
    
    </el-main>
    <div style="position: fixed; right: 10px; top: 90px; font-weight: 400; font-family: 宋体 " class="blink">
        <router-link to="/map">舆情谣言判断器</router-link>
    </div>
    
  </div>
</template>

<script>
import Common from './Common.vue';
import Loader from '../js/common.js'
import {Utils} from "../js/utils";
export default {
    name: 'Home',
    components: {Common},
    props: {
        msg: String
    },
    data(){
        return{
            title: "国内疫情",
            updateTime: '2020.02.15 02:29',
            sums: [
                {name: 'confirmed', text: '确诊', color: Utils.Colors[0], sum: 63951, add: "+19"},
                {name: 'suspected', text: '疑似', color: Utils.Colors[1], sum: 8228 , add: "+10"},
                {name: 'die', text: '死亡', color: Utils.Colors[2], sum: 1382 , add: "+1"},
                {name: 'ok', text: '治愈', color: Utils.Colors[3], sum: 7094, add: "+366"}
            ],
            tabs: [
                { 
                    label: "全国实时疫情", name: 'china', ids: ['ecChina', 'ecBar1'], level: 1, 
                    allTime: 0, data: null, mapName: 'china'
                },
                {
                    label: "省舆情回放", name: 'chinaTime', ids: ['ecChinaTime', 'ecBarTime1'], level: 1, 
                    allTime: 1, data: null, mapName: "china"
                },
                {
                    label: "省区实时疫情", name: 'province', ids: ['ecProvince', 'ecBar2'], level: 2, 
                    allTime: 0, data: null, mapName: "420000"
                },
                {
                    label: "时间序列回放", name: 'provinceTime', ids: ['ecProvinceTime', 'ecBarTime2'], 
                    level: 2, allTime: 1, data: null, mapName: '420000'
                }, 
                {
                    label: "曲线分析", name: "lineChina", ids: ['ecLineChina'], level: 1, isLine: 1, 
                    allTime: 1, data: null, mapName: "china"
                },
                {
                    label: "政策舆情时间线", name: "NewsTime", ids: ['ecWordCloud'], level: 1,  isWord: 1,
                    allTime: 1, data: null, mapName: "china"
                }
            ],
            loader: Loader,
            mapHeight: (Utils.getDevice() === 'xs') ? "330px" : "500px",
        }
    },
    mounted () {
        Loader.init(this.title, this.updateTime, this.sums, this.tabs);//this.title->国内确诊； this.update_time; this.sums->rough numbers; this.tabs 几个栏目
        [Loader.level, Loader.code] = [1, "86"];
        Loader.loadSummary(); //更新大致信息
        this.init();
console.log(this.$store.state);
console.log("vuex!");
    },
    methods: {
	click(index){
if (index==5) this.$store.state.showFooter= true;
else this.$store.state.showFooter=false;
console.log("givechange"+this.$store.state.showFooter);
Loader.handleClickTab(index);
},
        init () {
            Loader.activeName = "lineChina";
            Loader.loadData(this.tabs[4]);
        }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 0px 0 16px 0;
}

a {
  color: #42b983;
}

  .grid-content {
    border-radius: 4px;
    min-height: 46px;
  }
  .sum_numb {
      height: 20px;
      font-weight: 700;
  }
  .chart{
      min-height: 320px;
      margin-bottom: 20px;
  }

/* 定义keyframe动画，命名为blink */
@keyframes blink{
  0%{opacity: 1;}
  100%{opacity: 0;} 
}
/* 添加兼容性前缀 */
@-webkit-keyframes blink {
    0% { opacity: 1; }
    100% { opacity: 0; }
}
@-moz-keyframes blink {
    0% { opacity: 1; }
    100% { opacity: 0; }
}
@-ms-keyframes blink {
    0% {opacity: 1; } 
    100% { opacity: 0;}
}
@-o-keyframes blink {
    0% { opacity: 1; }
    100% { opacity: 0; }
}
/* 定义blink类*/
.blink{
    color: #dd4814 ;
    animation: blink 1s linear infinite;  
    /* 其它浏览器兼容性前缀 */
    -webkit-animation: blink 1s linear infinite;
    -moz-animation: blink 1s linear infinite;
    -ms-animation: blink 1s linear infinite;
    -o-animation: blink 1s linear infinite;
}
.blink>a{color: #dd4814!important}

</style>
