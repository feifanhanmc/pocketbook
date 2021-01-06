// pages/assetsAddStep1/assetsAddStep1.js
import regeneratorRuntime from '../..//utils/runtime/runtime';
import { request } from "../../utils/request/request.js";
import { login } from "../../utils/asyncwx.js";

Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 已选择的资产类型
    selectedAssetAcc: "", 
    selectedAssetIco: "other", 
    selectedAssetNam: "",
    selectedAssetTye: "",

    // 要创建的资产信息
    rmk_asset: "",
    amt_asset: 0.0,

    // OtherData
    assetIconPath: "/data/icons/asset/",
  },
  loadAssetInfo(){
    let pages = getCurrentPages();
    let currentPage = pages[pages.length - 1];
    let options = currentPage.options;
    const accAssetIndex = parseInt(options.accAssetIndex);
    const selectedAssetInfo = wx.getStorageSync('defaultAssetsList')[accAssetIndex]
    const {acc_asset, ico_asset, nam_asset, tye_asset} = selectedAssetInfo
    this.setData({
      selectedAssetAcc: acc_asset, 
      selectedAssetIco: ico_asset, 
      selectedAssetNam: nam_asset,
      selectedAssetTye: tye_asset
    })
  },
  handleInput1(e){
    const {value} = e.detail;
    this.setData({
      rmk_asset: value
    })
  },
  handleInput2(e){
    const {value} = e.detail;
    this.setData({
      amt_asset: value
    })
  },
  async handleSave(e){
    if(!this.data.rmk_asset){
      this.setData({
        rmk_asset: this.data.selectedAssetNam
      })
    }
    if(!this.data.amt_asset){
      this.setData({
        amt_asset: 0
      })
    }
    const addParams = {
      "nam_asset": this.data.selectedAssetNam,
      "rmk_asset": this.data.rmk_asset, 
      "amt_asset": this.data.amt_asset, 
      "tye_asset": this.data.selectedAssetTye,
      "ico_asset": this.data.selectedAssetIco}
    const {result} = await request({url:"/wxassets/add_assets",data:addParams,method:"post"});
    console.log(result)
    if(result){
      wx.setStorageSync('flagRefreshAssetsList', true);
      wx.setStorageSync('flagRefreshAccountData', true);
      wx.showToast({
        title: '添加成功！',
        icon: 'success',
        duration: 3000
      })
      wx.switchTab({
        url: '/pages/home/home',
      })
    }else{
      wx.showToast({
        title: '添加失败，请稍后再试！',
        icon: 'none',
        duration: 3000 
      })
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.loadAssetInfo()
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