<template>
<div>

    <div style="padding-top: 10px">
        <el-tabs v-model="activeName" @tab-click="handleClickTab">
            <!-- 标签页 -->
            <el-tab-pane :label="c.label" :name="c.name" v-for="(c, i) in tabs" :key="i">
                <el-row :gutter="5" v-if="i<4" v-show="activeName==c.name">
                    <!-- 地图 -->
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <div :id="c.ids[0]" class="chart" :style="{height: mapHeight}"></div>
                    </el-col>

                    <!-- 柱状图，可能太长，使用滚动条 -->
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <div class="chart" style="height: 500px">
                            <el-scrollbar style="height:100%">
                                <div :id="c.ids[1]" style="height:900px"></div>
                            </el-scrollbar>
                        </div>
                    </el-col>
                </el-row>
                <!-- 曲线分析 -->
                <!-- 舆情-->
                <el-row v-else v-show="1==1">
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <div :id="c.ids[0]" class="chart" style="height: 500px"></div>
                    </el-col>
                </el-row>
            </el-tab-pane>
        </el-tabs>
    </div>
<div v-if='ifnews==true'>
<light-timeline :items='items'></light-timeline>
</div>
    <div style="height: 20px"></div>
</div>
</template>

<script>
import {Utils} from "../js/utils";
import {API} from "../js/server";

export default {
    name: 'Common',

    props: {
        title: String,

        updateTime: String,
        sums: Array,
        tabs: Array,
        activeName_: String
    },
    data () {
        return {
ifnews:false,
            items:[{'tag':'1-2-3','content':'1-2-3'}],
            activeName: '',
            mapHeight: (Utils.getDevice() === 'xs') ? "330px" : "500px"
        }
    },
computed: {
listenstore(){
return this.$store.state.showFooter;
}
},
mounted(){
this.init();
},
    watch: {
listenstore: function(){
console.log("listen_change"+this.$store.state.showFooter)
if (this.$store.state.showFooter){
this.ifnews=true;
}
else{
this.ifnews=false;
}
},
        activeName_ (v) {
            this.activeName = v;
        }
    },
    methods: {
        init(){

 let $this = this;
          let key = API.GetNews;
            Utils.ajaxData(key, {'need':'none'}, function (rst) {
let i =0;
	$this.items=rst.data;
for (i=0;i<rst.data.length;i++){
$this.items[i]['tag']='2020年3月20日';
$this.items[i]['content']=rst.data[i].title + rst.data[i]['summary'];

}


            });
},
        handleClickTab: function (p) {
            this.$emit("handleClickTab", parseInt(p.index));
        }
    }
}
</script>

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


</style>
