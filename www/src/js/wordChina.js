import {Utils} from "../js/utils";
import getTimeline from "./timeline";

let superOption = {
    baseOption: {
        timeline: getTimeline()
    },
    options: []
};

let chart = {
    name: "china",
    option: null,
    superOption: superOption,
    initData: null,
    instance: null,
    useMaxValue: true
}
// 针对事件序列数据，数据上升一个维度
// param:   dts : {'2020-02-01': []}
function getOption (srcData, _option) {
	let i=0;
	let data=[];
	for (i=0;i<srcData.length;i++)
	data.push({name: srcData[i], value:100})
    _option.title.text = "热点舆论" 
    _option.series[0]['data'] = data;
    _option.series[0]['type']='wordCloud';
        _option.series[1]['data'] = [[0,0]];
    _option.series[1]['type']='scatter';
    _option.series[1]['symbolSize']= 1;
    _option.series[1]['label']={
                normal: {
                    show: true,
   formatter: '{titleBg|截至2月2日18时，全国累计报告确诊病例}',
rich: {
    titleBg: {
        align: 'right',
        backgroundColor: '#eee',
        height: 100,
        borderRadius: [0, 0, 0, 0],
        padding: [0, 0, 0, 0],
        width: 2500,
        color: '#000'
    }},

                }
            }

    return _option;
}
function getOptions () {
	let  dts = {'2020-02-01': ['双黄连','方舱','粮食'],'2020-02-02':['蝙蝠','蝗虫','穿山甲','双黄连','封城日记'],'2020-02-03':['境外','关门'],'2020-02-04':['A股','黄金']} //
    let tms = Object.keys(dts);
    superOption.baseOption.timeline.data = tms;
    superOption.options = tms.map(k => {
        let _option = { title: {text: '', top: 55, textStyle: {color: '#bbb', fontSize: 16}}, series: [{},{}], xAxis: {
        axisLabel: {show: false},
        axisLine: {show: false},
        splitLine: {show: false},
        axisTick: {show: false},
        min: 0,
        max: 1
    },
    yAxis: {
        axisLabel: {show: false},
        axisLine: {show: false},
        splitLine: {show: false},
        axisTick: {show: false},
        min: 0,
        max: 1
    }};
        return getOption(dts[k], _option);
    });
	superOption.baseOption.timeline.autoPlay = false;
	superOption.baseOption.timeline.currentIndex = tms.length - 1;
	return superOption;
    // 理论上讲tms是有序的，若不是则应在此处排序
    /*
    let tms = Object.keys(dts);
    superOption.baseOption.timeline.data = tms;
    superOption.options = tms.map(k => {
        let _option = { title: {text: '', top: 55, textStyle: {color: '#bbb', fontSize: 16}}, series: [{}]};
        return getOption(dts[k], mapName, _option);
    });
    superOption.baseOption.timeline.autoPlay = false;
    superOption.baseOption.timeline.currentIndex = tms.length - 1;
    return superOption;*/



}

chart.initData = function (id) {
		console.log("cloud");
        let _option = getOptions();
        console.log(_option);
        console.log("option!");



    
    chart.instance = Utils.drawGraph(_option, id);
    return chart.instance;
};

let chartWord = chart;
export default chartWord;