// pages/bill/bill.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";
import uCharts from '../../utils/u-charts.js';

Page({

  /**
   * 页面的初始数据
   */
  data: {   
    // TransData
    transList: [],

    // ReportData
    days: [],
    expend: [],
    income: [],

    // ImageData
    imageNoDataBill: "nodata_bill",

    // OtherData
    tranIconPath: "/data/icons/tran/",
    nodataIconPath: "/data/icons/nodata/",
  },
  handleModifyTrans(e){
    const index = parseInt(e.currentTarget.id)
    const trans = this.data.transList[index]
    console.log(trans)
    const {tye_flow} = trans
    if(tye_flow=='adjust'){
      wx.showToast({
        title: '仅支持长按删除',
        icon: 'none',
        duration: 3000 
      })
    }else{
      wx.navigateTo({
        url: "/pages/transModify/transModify?transStr="+JSON.stringify(trans)
      })
    }   
  },
  async showTransList() {
    const {trans} = await request({url:"/wxtrans/show_trans",data:{},method:"post"});
    this.setData({
      transList: trans
    })
    wx.setStorageSync('transList', trans)
    wx.setStorageSync('flagRefreshTransData', false)
  },
  genReport(id, data, name, color, windowWidth){
    // 生成图表
    new uCharts({
      $this:this,
      canvasId: id,
      type: 'column',
      categories: this.data.days,
      dataPointShape: false,
      legend: {show:false},
      series: [{
          name: name,
          data: data,
          color: color,
          format: function (val) {
            if(val==0){ return '' }
            return val
          }
      }],
      yAxis: {
          max: Math.max(...data)*1.1,
          title: '金额',
          min: 0,
          gridColor: '#ffffff',
          disabled: true,
      },
      xAxis:{
        disableGrid: true,
        labelCount:15,
      },
      width: windowWidth,
      height: 120,
    });
  },
  async showReport() {  
    const {report} = await request({url:"/wxtrans/show_flow",data:{},method:"post"});
    const {days, expend, income} = report;
    this.setData({
      days,
      expend,
      income,
    })
    wx.setStorageSync('billReport', report)
    // 获取屏幕宽度
    let windowWidth = 320;
    try {
        let res = wx.getSystemInfoSync();
        windowWidth = res.windowWidth;
    } catch (e) {
      console.log(e)
    }
    this.genReport('lineCanvasExpend', this.data.expend, '流出', '#ff0000', windowWidth)
    this.genReport('lineCanvasIncome', this.data.income, '流入', '#008000', windowWidth)
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
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
    if(wx.getStorageSync('flagRefreshTransData')){
      this.showTransList()
      this.showReport()
    }else{
      const {days, income, expend} = wx.getStorageSync('billReport')
      this.setData({
        transList: wx.getStorageSync('transList'),
        days,
        expend,
        income,
      })
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