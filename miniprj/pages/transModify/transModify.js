// pages/transAdd/transAdd.js
import regeneratorRuntime from '../../utils/runtime/runtime';
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

    // 转入信息
    modifyFlag: false,

    // SelectedTransData
    nam_asset: "",
    rmk_asset: "",
    acc_asset: "",
    ico_asset: "",
    amt_trans: 0.0,
    cod_trans_type: "", 
    tye_asset: "",
    tye_flow: "", 
    txt_trans_type: "", 
    ico_trans: "",
    dte_trans: "",
    txt_remark: "",
    acc_asset_related: "",
    nam_asset_related: "",
    rmk_asset_related: "",
    ico_asset_related: "",
    tye_asset_related: "",
    
    // AssetDataPicker
    assetsListPicker: [],
    indexPicker: 0,
    indexPicker2: 0,

    // TransTypeData
    expendTranstypes: [],
    incomeTranstypes: [],
    transferTranstypes: [],

    // IconData
    assetIconPath: "/data/icons/asset/",
    tranIconPath: "/data/icons/tran/",
    otherIconPath: "/data/icons/other/",
    transferIco: "transfer",

    // TabsData
    tabs: ['流出', '流入', '转账'],

    // SystemData
    winWidth: 0,
    winHeight: 0,
    currentTab: 0,
    swiperViewHeight: 0,
  },
  loadAssetInfo(){
    let pages = getCurrentPages();
    let currentPage = pages[pages.length - 1];
    const opt = currentPage.options
    if(JSON.stringify(opt)!='{}'){  // 有参数则表明从Modify页面跳转而来
      this.setData({modifyFlag: true})
      const trans = JSON.parse(opt.transStr);
      console.log(trans)
      const {acc_asset, nam_asset, rmk_asset, ico_asset, amt_trans, cod_trans_type, ico_trans,tye_flow, acc_asset_related, nam_asset_related, rmk_asset_related, ico_asset_related, tye_asset_related} = trans
      this.setData({
        acc_asset, nam_asset, rmk_asset, ico_asset, amt_trans, cod_trans_type, ico_trans,tye_flow, acc_asset_related, nam_asset_related, rmk_asset_related, ico_asset_related, tye_asset_related
      })

    } 
  },
  bindPickerChange: function(e) {
    const indexPicker = parseInt(e.detail.value)
    const {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset} = this.data.assetsListPicker[indexPicker]
    this.setData({
      indexPicker,
      lastTransAssetAcc: acc_asset,
      lastTransAssetIco: ico_asset,
      lastTransAssetNam: nam_asset,
      lastTransAssetRmk: rmk_asset,
      lastTransAssetTye: tye_asset,
      acc_asset,
      ico_asset,
      nam_asset,
      rmk_asset,
      tye_asset,
    })
  },
  bindPickerChange2: function(e) {
    const indexPicker2 = parseInt(e.detail.value)
    const {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset} = this.data.assetsListPicker[indexPicker2]
    this.setData({
      indexPicker2,
      acc_asset_related: acc_asset,
      nam_asset_related: nam_asset,
      rmk_asset_related: rmk_asset,
      ico_asset_related: ico_asset,
      tye_asset_related: tye_asset,
    })
  },
  handleInputAmt(e){
    this.setData({
      amt_trans: e.detail.value
    })
  },
  handleAddAsset(e){
    wx.navigateTo({
      url: '/pages/assetsAdd/assetsAdd',
    })
  },
  bindDateChange: function(e) {
    this.setData({
      dte_trans: e.detail.value.replace(/-/g,'')
    })
  },
  handleInputRemark(e){
    this.setData({
      txt_remark: e.detail.value
    })
  },
  async handleSave(e){
    if(this.data.amt_trans==0){
      wx.showToast({
        title: '请输入金额',
        icon: 'none',
        duration: 3000 
      })
      return false;
    }
    // 转账不需要选择交易类型；支出、收入需要
    if(this.data.currentTab==2){
      if(this.data.acc_asset==this.data.acc_asset_related){
        wx.showToast({
          title: '请选择不同资产账户',
          icon: 'none',
          duration: 3000 
        })
        return false;
      }
      // 转账的交易类型中还分很多种，默认索引为0的类型
      const {cod_trans_type, tye_flow, txt_trans_type, ico_trans} = wx.getStorageSync('transferTranstypes')[0]
      this.setData({
        cod_trans_type,
        tye_flow,
        txt_trans_type,
        ico_trans,
      })
    }else{
      if(!this.data.cod_trans_type){
        wx.showToast({
          title: '请选择'+ this.data.tabs[this.data.currentTab] +'类型',
          icon: 'none',
          duration: 3000 
        })
        return false;
      }
      this.setData({
        acc_asset_related: "",
        nam_asset_related: "",
        rmk_asset_related: "",
        ico_asset_related: "other",
        tye_asset_related: "",

      })
    }

    const transAddParmas = {
      acc_asset: this.data.acc_asset,
      nam_asset: this.data.nam_asset,
      rmk_asset: this.data.rmk_asset,
      amt_trans: this.data.amt_trans,
      tye_asset: this.data.tye_asset,
      tye_flow: this.data.tye_flow,
      dte_trans: this.data.dte_trans,
      acc_asset_related: this.data.acc_asset_related,
      nam_asset_related: this.data.nam_asset_related,
      rmk_asset_related: this.data.rmk_asset_related,
      ico_asset_related: this.data.ico_asset_related,
      tye_asset_related: this.data.tye_asset_related,
      cod_trans_type: this.data.cod_trans_type,    
      txt_trans_type: this.data.txt_trans_type,
      txt_remark: this.data.txt_remark,
      ico_trans: this.data.ico_trans
    }
    const {result} = await request({url:"/wxtrans/add_trans",data:transAddParmas,method:"post"});

    // 保存成功后，更新lastTransData，并设置相关flagRefresh为true
    if(result){
      wx.showToast({
        title: '保存成功',
        icon: 'success',
        duration: 3000 
      })
      wx.setStorageSync('lastTransData', {
        acc_asset: this.data.acc_asset,
        nam_asset: this.data.nam_asset,
        rmk_asset: this.data.rmk_asset,
        ico_asset: this.data.ico_asset,
        tye_asset: this.data.tye_asset,
      })

      wx.setStorageSync('flagRefreshAssetsList', true)
      wx.setStorageSync('flagRefreshStatisticsData', true)
      wx.setStorageSync('flagRefreshTransData', true)
      wx.setStorageSync('flagRefreshReportData', true)
      wx.setStorageSync('flagRefreshCurrentAssetTransData', true)

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
  // 动态设置交易类型icon栏目的高度
  handleSetSwiperHeight(){
    if(this.data.currentTab==0){
      this.setData({swiperViewHeight: (parseInt(wx.getStorageSync('expendTranstypes').length/6)+1)*150})
    }else if(this.data.currentTab==1){
      this.setData({swiperViewHeight: (parseInt(wx.getStorageSync('incomeTranstypes').length/6)+1)*150})
    }else{
      this.setData({swiperViewHeight: 200})
    }
  },
  async handleShowTranstypes(e) {
    if(wx.getStorageSync('flagRefreshTranstypesData')){
      const {transtypes} = await request({url:"/wxtranstypes/show_transtypes",data:{},method:"post"});
      const {expend, income, transfer} = transtypes
      wx.setStorageSync('expendTranstypes', expend)
      wx.setStorageSync('incomeTranstypes', income)
      wx.setStorageSync('transferTranstypes', transfer)
      wx.setStorageSync('flagRefreshTranstypesData', false)
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
  handleInitRelatedData(){
    if(wx.getStorageSync('assetsList').length>0){
      const {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset} = wx.getStorageSync('assetsList')[0]
      this.setData({
        acc_asset_related: acc_asset,
        nam_asset_related: nam_asset,
        rmk_asset_related: rmk_asset,
        ico_asset_related: ico_asset,
        tye_asset_related: tye_asset,
      })
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;

    // 加载跳转页面传递过来的信息
    this.loadAssetInfo()

    // 初始化LastTransData
    if(!wx.getStorageSync('lastTransData')){
      if(wx.getStorageSync('assetsList').length>0){
        const {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset} = wx.getStorageSync('assetsList')[0]
        wx.setStorageSync('lastTransData', {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset})
      }else{ // 还没有资产账户
      }
    }

    // 初始化assetsListPicker，第一条为最近的一笔交易相关的asset信息
    var assetsListPicker = []
    const {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset} = wx.getStorageSync('lastTransData')
    assetsListPicker.push({
      'nam_pick': nam_asset + ' | ' + rmk_asset,
      'acc_asset': acc_asset, 
      'nam_asset': nam_asset,
      'rmk_asset': rmk_asset, 
      'ico_asset': ico_asset,
      'tye_asset': tye_asset,
    })
    wx.getStorageSync('assetsList').forEach(function (asset) {
      const {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset} = asset
      if(acc_asset!=assetsListPicker[0].acc_asset){
        assetsListPicker.push({
          'nam_pick': nam_asset + ' | ' + rmk_asset,
          'acc_asset': acc_asset, 
          'nam_asset': nam_asset,
          'rmk_asset': rmk_asset, 
          'ico_asset': ico_asset,
          'tye_asset': tye_asset,
        })
      }
    });
    this.setData({
      assetsListPicker: assetsListPicker
    })

    // 初始化related账户数据
    this.handleInitRelatedData()

    // 获取当前设备的宽高
    wx.getSystemInfo( {
        success: function( res ) {
            that.setData( {
                winWidth: res.windowWidth,
                winHeight: res.windowHeight
            });
        }
    });

    // 初始化日期为今天日期
    const today = new Date()
    const month = today.getMonth()+1
    const day = today.getDate()
    var dateList = [today.getFullYear()]
    if(month<10){
      dateList.push("0", month)
    }else{
      dateList.push(month)
    }
    if(day<10){
      dateList.push("0", day)
    }else{
      dateList.push(day)
    }
    this.setData({
      dte_trans: dateList.join("")
    })
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
      // Modify
      if(this.data.modifyFlag){ // 若modifyFlag为true，则说明是Modify


      }else{// 若modifyFlag为false，则说明不是Modify，是Add
        const {acc_asset, nam_asset, rmk_asset, ico_asset, tye_asset} = wx.getStorageSync('lastTransData')
        this.setData({
          acc_asset,
          ico_asset,
          nam_asset,
          rmk_asset,
          tye_asset,
          lastTransAssetAcc: acc_asset,
          lastTransAssetIco: ico_asset,
          lastTransAssetNam: nam_asset,
          lastTransAssetRmk: rmk_asset,
          lastTransAssetTye: tye_asset,
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