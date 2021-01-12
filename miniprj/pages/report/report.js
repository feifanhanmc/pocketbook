// pages/report/report.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";
var wxCharts = require('../../utils/wxcharts')

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // DatePickerData
    datePicker: [],
    monthList: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'ALL'],
    index:[0, 0],
    
    // ReportData
    report: [],
    nameList: ['流出', '流入', '转账'],
    colorList: ['#ff0000', '#008000', '#000000'],
    indexReport: 0,
    currentReport: [],

    // SystemData
    windowWidth: 320,

    // OtherData
    tranIconPath: "/data/icons/tran/",
  },
  handleChange(e){
    const indexReport = (this.data.indexReport+1)%3
    this.setData({
      indexReport,
      currentReport: this.data.report[indexReport]
    })
    this.showRingReport(this.data.report, this.data.indexReport)
  },
  bindPicker:function(e){
    const index = e.detail.value
    this.setData({
      index,
    })
  },
  extractPieData(rawData){
    var pie = []
    for (var i=0;i<rawData.length;i++) {
      const {txt_trans_type, amount} = rawData[i]
      pie.push({'name': txt_trans_type, 'data': amount})
    }
    return pie
  },
  showRingReport(report, indexReport){
    const series = this.extractPieData(report[indexReport])
    const name = this.data.nameList[indexReport]
    new wxCharts({
      canvasId: 'ringCanvas',
      animation: true,
      type: 'ring',
      series: series,    
      title: {
        name: name,
        color: this.data.colorList[indexReport],
        fontSize: 10,
      },
      subtitle: {
        name: '⇌',
        color: '#FABD03',
        fontSize: 9,
      },
      legend: false,
      dataLabel: true,
      width: this.data.windowWidth,
      height: 100,
    });
  },
  async loadReport(){
    const year = this.data.datePicker[0][this.data.index[0]]
    const month = this.data.datePicker[1][this.data.index[1]],
    showParams = {'year': year, 'month': month}
    const {report} = await request({url:"/wxtrans/show_report",data:showParams,method:"post"});
    this.setData({
      report,
      currentReport: report[this.data.indexReport]
    })
    wx.setStorageSync('reportData', report)
    wx.setStorageSync('flagRefreshReportData', false)

    this.showRingReport(this.data.report, this.data.indexReport)
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 初始化选择器数据
    const date = new Date()
    const year = parseInt(date.getFullYear())
    const month = date.getMonth()
    var yearList = []
    for (let count = 5; count >= 0; count--) {
      yearList.push(year-count)      
    }
    this.setData({
      datePicker: [yearList, this.data.monthList],
      index: [5, month]
    })

    // 获取屏幕宽度
    try {
        let res = wx.getSystemInfoSync();
        const windowWidth = res.windowWidth;
        this.setData({windowWidth})
    } catch (e) {
      console.log(e)
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    // 准备数据
    if(!wx.getStorageSync('reportData')){
      this.loadReport()
    }else{
      const report = wx.getStorageSync('reportData')
      this.setData({
        report,
        currentReport: report[this.data.indexReport]
      })
      this.showRingReport(this.data.report, this.data.indexReport)
    }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})