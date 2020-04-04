<template>
  <div>

  
    <el-menu
      
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      @select="handleSelect"
      background-color="#EFEEEA"
      text-color="#241c15"

      :collapse="isCollapse"
      :active = "seled"
      active-text-color="#ffd04b">
      <el-menu-item index="1">
        <template slot="title">
          <i class="el-icon-s-platform"></i>
          <span>全国疫情</span>
        </template>

      </el-menu-item>

   
      <el-menu-item index="2">

        <template slot="title">
          <i class="el-icon-message-solid"></i>
          <span>谣言专栏</span>
  
        </template>

            </el-menu-item>      
    <el-menu-item index="3">

        <template slot="title">
          <i class="el-icon-message-solid"></i>
          <span>舆情分析</span>
  
        </template>

            </el-menu-item>      
  
  

        <el-menu-item index="4">

        <template slot="title">
          <i class="el-icon-message-solid"></i>
          <span>新闻搜索</span>
  
        </template>

            </el-menu-item>      
  
  
    </el-menu>


  </div>
</template>
<script>
  export default {
     data() {
    return {
      defaultAactiveIndex: "", //默认打开的菜单的索引----必须是字符串
      openeds: ["0"], //展开菜单项的索引
      oldmenu: [], //所有的菜单
      isCollapse: false, //是否折叠
      searchMenuVal: "", //搜索关键字
      menus: [], //显示的菜单
      searchMenus: [], //搜索时的菜单
      seled:1
    };
  },
    methods: {
      handleOpen() {
       //         if (key==4)
       //   this.router.push('Map')
      //  console.log("open");
      //  console.log(key, keyPath);
      },
      handleClose() {
     //           if (key==4)
     //     this.router.push('Map')
     //          console.log("close");
      //  console.log(key, keyPath);
      },
      handleSelect(key) {
        if (key==1) {
          this.$router.push('china');
          this.seled=1;
        }
        if (key==2)
          {this.$router.push('Map');
            this.seled=2;}
        if (key==3)
          { console.log("ANA");
            this.$router.push('Ana');
            this.seled=3;}
        if (key ==4){
          this.$router.push('News');
            this.seled=4;}
        

             //   console.log(key+keyPath);
              
      //  console.log(key, keyPath);
      }
    }
  }
</script>
