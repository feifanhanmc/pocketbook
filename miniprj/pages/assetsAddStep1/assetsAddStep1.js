// pages/assetsAddStep1/assetsAddStep1.js
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
    const accAssetId = parseInt(options.accAssetId)-1;
    const selectedAssetInfo = wx.getStorageSync('defaultAssetsList')[accAssetId]
    const {acc_asset, ico_asset, nam_asset, tye_asset} = selectedAssetInfo
    this.setData({
      selectedAssetAcc: acc_asset, 
      selectedAssetIco: ico_asset, 
      selectedAssetNam: nam_asset,
      selectedAssetTye: tye_asset
    })
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