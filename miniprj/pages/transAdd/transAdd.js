// pages/transAdd/transAdd.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // LastData
    lastTransAssetAcc: "",
    lastTransAssetIco: "",
    lastTransAssetNam: "",
    lastTransAssetRmk: "",
    
    // TransData
    acc_asset: "",
    amt_trans: 0.0,
    
    // TransTypeData
    transTypeList: [],

    // OtherData
    assetIconPath: "/data/icons/asset/",
    tranIconPath: "/data/icons/tran/",

    winWidth: 0,
    winHeight: 0,
    currentTab: 0,

    s1: 1,
    s2: 2,
    s3: 3,

    tabs: [
      {
        id: 0,
        name: "流出",
        isActive: true
      },
      {
        id: 1,
        name: "流入",
        isActive: false
      }
      ,
      {
        id: 2,
        name: "转账",
        isActive: false
      }
    ]
  },
  handleInputAmt(e){

  },
  async handleShowTranstypes(e) {
    const {transtypes} = await request({url:"/wxtranstypes/show_transtypes",data:{},method:"post"});
    const {expend, income, transfer} = transtypes
    wx.setStorageSync('expendTranstypes', expend)
    wx.setStorageSync('incomeTranstypes', income)
    wx.setStorageSync('transferTranstypes', transfer)
  },
  // tab切换逻辑
  swichNav: function( e ) {
    var that = this;
    if( this.data.currentTab === e.target.dataset.current ) {
        return false;
    } else {
        that.setData( {
            currentTab: e.target.dataset.current
        })
    }
  },
  bindChange: function( e ) {
      var that = this;
      that.setData( { currentTab: e.detail.current });
  },
  handleItemChange(e) {
    // 接收传递过来的参数
    const { index } = e.detail;
    let { tabs } = this.data;
    tabs.forEach((v, i) => i === index ? v.isActive = true : v.isActive = false);
    this.setData({
      tabs
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // 初始化LastTransData
    if(!wx.getStorageSync('lastTransData')){
      const {acc_asset, nam_asset, rmk_asset, ico_asset} = wx.getStorageSync('assetsList')[0]
      const lastTransData = {acc_asset, nam_asset, rmk_asset, ico_asset}
      wx.setStorageSync('lastTransData', lastTransData)
    }

    // 初始化TransTypeData
    if(!wx.getStorageSync('transTypeList')){
      this.handleShowTranstypes()
    }



    var that = this;

    /**
     * 获取当前设备的宽高
     */
    wx.getSystemInfo( {

        success: function( res ) {
            that.setData( {
                winWidth: res.windowWidth,
                winHeight: res.windowHeight
            });
        }

    });
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
    // Modify 初始化数据
    // 更新acc_asset

    // 若acc_asset为空，则说明不是Modify，是Add
    if(!this.data.acc_asset){
      const {acc_asset, nam_asset, rmk_asset, ico_asset} = wx.getStorageSync('lastTransData')
      this.setData({
        lastTransAssetAcc: acc_asset,
        lastTransAssetIco: ico_asset,
        lastTransAssetNam: nam_asset,
        lastTransAssetRmk: rmk_asset
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