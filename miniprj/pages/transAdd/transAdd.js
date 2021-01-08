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
    
    // SelectedTransData
    acc_asset: "",
    amt_trans: 0.0,
    cod_trans_type: "", 
    tye_flow: "", 
    txt_trans_type: "", 
    ico_trans: "",

    // TransTypeData
    expendTranstypes: [],
    incomeTranstypes: [],
    transferTranstypes: [],

    // IconData
    assetIconPath: "/data/icons/asset/",
    tranIconPath: "/data/icons/tran/",

    // SystemData
    winWidth: 0,
    winHeight: 0,
    currentTab: 0,
    swiperViewHeight: 0,
  },
  handleInputAmt(e){

  },
  handleAddAsset(e){
    wx.navigateTo({
      url: '/pages/assetsAddStep0/assetsAddStep0',
    })
  },
  // 动态设置交易类型icon栏目的高度
  handleSetSwiperHeight(){
    if(this.data.currentTab==0){
      this.setData({swiperViewHeight: (parseInt(wx.getStorageSync('expendTranstypes').length/6)+1)*150})
    }else if(this.data.currentTab==1){
      this.setData({swiperViewHeight: (parseInt(wx.getStorageSync('incomeTranstypes').length/6)+1)*150})
    }else{
      this.setData({swiperViewHeight: (parseInt(wx.getStorageSync('transferTranstypes').length/6)+1)*150})
    }
  },
  async handleShowTranstypes(e) {
    if(wx.getStorageSync('flagRefreshTranstypesData')){
      const {transtypes} = await request({url:"/wxtranstypes/show_transtypes",data:{},method:"post"});
      const {expend, income, transfer} = transtypes
      wx.setStorageSync('expendTranstypes', expend)
      wx.setStorageSync('incomeTranstypes', income)
      wx.setStorageSync('transferTranstypes', transfer)
      wx.setStorageSync('flagRefreshTranstypesDatakey', false)
    }
    this.setData({
      expendTranstypes: wx.getStorageSync('expendTranstypes'),
      incomeTranstypes: wx.getStorageSync('incomeTranstypes'),
      transferTranstypes: wx.getStorageSync('transferTranstypes'),
    })
    this.handleSetSwiperHeight()

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
      that.setData({ 
        currentTab: e.detail.current 
      });
      this.handleSetSwiperHeight()

  },
  handleChoseTranstype(e){
    const {index} = e.target.dataset;
    const expendLen = this.data.expendTranstypes.length
    const incomeLen = this.data.incomeTranstypes.length
    const transferLen = this.data.transferTranstypes.length
    var transtypeChose = {}
    if(index<expendLen){
      var transtypeChose = this.data.expendTranstypes[index]
    }else if(index<(expendLen+incomeLen)){
      var transtypeChose = this.data.incomeTranstypes[index-expendLen]
    }else{
      var transtypeChose = this.data.transferTranstypes[index-incomeLen-expendLen]
    }
    const {cod_trans_type, tye_flow, txt_trans_type, ico_trans} = transtypeChose;
    this.setData({
      cod_trans_type, tye_flow, txt_trans_type, ico_trans
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;

    // 初始化LastTransData
    if(!wx.getStorageSync('lastTransData')){
      if(wx.getStorageSync('assetsList').length>0){
        const {acc_asset, nam_asset, rmk_asset, ico_asset} = wx.getStorageSync('assetsList')[0]
        const lastTransData = {acc_asset, nam_asset, rmk_asset, ico_asset}
        wx.setStorageSync('lastTransData', lastTransData)
      }else{ // 还没有资产账户
        wx.setStorageSync('lastTransData', {})
      }
    }

    // 设置TranstypeData更新Flag
    wx.setStorageSync('flagRefreshTranstypesData', true)

    // 获取当前设备的宽高
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
    if(wx.getStorageSync('assetsList').length>0){
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
      
      // 加载交易类型数据
      this.handleShowTranstypes()
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