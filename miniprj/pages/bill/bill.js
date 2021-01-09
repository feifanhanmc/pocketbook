// pages/bill/bill.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // flagRefreshTransData
    
    // TransData
    transList: [],

    // ImageData
    imageNoDataBill: "nodata_bill",

    // OtherData
    tranIconPath: "/data/icons/tran/",
    nodataIconPath: "/data/icons/nodata/",
  },
  async showTransList() {
    const {trans} = await request({url:"/wxtrans/show_trans",data:{},method:"post"});
    this.setData({
      transList: trans
    })
    wx.setStorageSync('transList', trans)
    wx.setStorageSync('flagRefreshTransData', false)
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
    }else{
      this.setData({
        transList: wx.getStorageSync('transList')
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